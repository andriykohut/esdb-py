from __future__ import annotations

import asyncio
import base64
import contextlib
import enum
import itertools
import logging
import random
import urllib.parse
from dataclasses import dataclass
from functools import cmp_to_key
from typing import AsyncContextManager, Optional, Union

import grpc

from esdb.exceptions import DiscoveryError
from esdb.generated.gossip_pb2_grpc import GossipStub
from esdb.generated.persistent_pb2_grpc import PersistentSubscriptionsStub
from esdb.generated.streams_pb2_grpc import StreamsStub
from esdb.gossip import Gossip, Member, State
from esdb.streams import Streams
from esdb.subscriptions import PersistentSubscriptions

logger = logging.getLogger(__name__)


class Preference(enum.Enum):
    LEADER = enum.auto()
    FOLLOWER = enum.auto()
    READ_ONLY_REPLICA = enum.auto()


class BasicAuthPlugin(grpc.AuthMetadataPlugin):
    def __init__(self, user: str, password: str) -> None:
        self.__auth = base64.b64encode(f"{user}:{password}".encode())

    def __call__(self, context: grpc.AuthMetadataContext, callback: grpc.AuthMetadataPluginCallback) -> None:
        callback((("authorization", b"Basic " + self.__auth),), None)


@dataclass
class Connection:
    channel: grpc.aio._base_channel.Channel  # type: ignore
    streams: Streams
    subscriptions: PersistentSubscriptions
    gossip: Gossip


def pick_node(preference: Preference, members: list[Member]) -> Optional[Member]:
    preference_map = {
        Preference.LEADER: [State.Leader],
        Preference.FOLLOWER: [State.Follower],
        Preference.READ_ONLY_REPLICA: [State.ReadOnlyLeaderless, State.PreReadOnlyReplica, State.ReadOnlyReplica],
    }
    preferred_states = preference_map[preference]

    def _compare(a: Member, b: Member) -> int:
        return (preferred_states.index(b.state) if b.state in preferred_states else -1) - (
            preferred_states.index(a.state) if a.state in preferred_states else -1
        )

    members_ = members.copy()
    random.shuffle(members_)

    member: Optional[Member] = next(
        (
            m
            for m in sorted(members_, key=cmp_to_key(_compare))
            if m.is_alive and m.state in list(itertools.chain(*preference_map.values())) and m.endpoint
        ),
        None,
    )
    if not member or not member.endpoint:
        return None
    return member


def parse_endpoint(s: str) -> tuple[str, int]:
    if ":" in s:
        items = s.split(":")
        if len(items) != 2:
            raise ValueError("Too many colons in a host")
        host, port_str = items
        try:
            port = int(port_str)
        except ValueError:
            raise ValueError(f"{port_str} port is not a number")
        return host, port

    return s, 2113


def parse_connection_string(connection_string: str) -> dict:
    "esdb://dwqdqw:2113,dwqdq:2113,dqwdwq:2113?keepAliveTimeout=10000&keepAliveInterval=10000"
    config = {}
    scheme, rest = connection_string.split("://")
    if scheme not in ("esdb", "esdb+discover"):
        raise ValueError("esdb:// or esdb+discover:// scheme is required")

    config["dns_discover"] = scheme == "esdb+discover"

    if "@" in rest:
        user_info, rest = rest.split("@")
        user_info_items = user_info.split(":")
        if len(user_info) != 2:
            raise ValueError("Invalid user credentials")
        user, password = user_info_items
        if not user:
            raise ValueError("Username is required")
        if not password:
            raise ValueError("Password is required")
        config.update({"user": user, "password": password})

    hosts, *queries = rest.split("?")
    endpoints = []
    for host in hosts.split(","):
        endpoints.append(parse_endpoint(host))
    if len(endpoints) == 1:
        config["address"] = endpoints[0]
    else:
        config["gossip_seed"] = endpoints

    if queries:
        [settings_query] = queries
        settings = {}
        for key, val in urllib.parse.parse_qs(settings_query, strict_parsing=True).items():
            if len(val) != 1:
                raise ValueError(f"Too many values for {key}")
            settings[key] = val[0]
        config['settings'] = settings

    return config


class ESClient:
    def __init__(
        self,
        endpoints: Union[str, list[str]],
        username: Optional[str] = None,
        password: Optional[str] = None,
        insecure: bool = False,
        root_certificates: Optional[bytes] = None,
        private_key: Optional[bytes] = None,
        certificate_chain: Optional[bytes] = None,
        keepalive_time_ms: int = 10000,
        keepalive_timeout_ms: int = 10000,
        discover: bool = False,
        discovery_interval: int = 100,
        discovery_attempts: int = 10,
        gossip_timeout: int = 5,
        node_preference: Preference = Preference.LEADER,
    ) -> None:
        self.channel_credentials = None
        self.call_credentials = None
        self.insecure = insecure
        self.endpoints = endpoints if isinstance(endpoints, list) else [endpoints]
        self.discover = discover
        self.discovery_interval = discovery_interval
        self.discovery_attempts = discovery_attempts
        self.gossip_timeout = gossip_timeout
        self.node_preference = node_preference

        self.options = [
            ("grpc.keepalive_time_ms", keepalive_time_ms),
            ("grpc.keepalive_timeout_ms", keepalive_timeout_ms),
        ]

        if not self.insecure:
            self.channel_credentials = grpc.ssl_channel_credentials(
                root_certificates=root_certificates,
                private_key=private_key,
                certificate_chain=certificate_chain,
            )

        if any([username, password]) and not all([username, password]):
            raise ValueError("Both username and password are required")

        if username and password:
            self.call_credentials = grpc.metadata_call_credentials(BasicAuthPlugin(username, password), name="auth")

    def _create_channel(self, endpoint: str) -> grpc.aio.Channel:  # type: ignore
        if self.insecure:
            return grpc.aio.insecure_channel(endpoint, options=self.options)  # type: ignore
        assert self.channel_credentials
        credentials = (
            grpc.composite_channel_credentials(self.channel_credentials, self.call_credentials)
            if self.call_credentials
            else self.channel_credentials
        )
        return grpc.aio.secure_channel(endpoint, credentials, self.options)  # type: ignore

    @contextlib.asynccontextmanager  # type: ignore
    async def connect(self) -> AsyncContextManager[Connection]:  # type: ignore
        endpoint = self.endpoints[0]
        if self.discover:
            endpoint = await self.discover_endpoint()

        async with self._create_channel(endpoint) as channel:
            yield Connection(
                channel=channel,
                streams=Streams(StreamsStub(channel)),
                subscriptions=PersistentSubscriptions(PersistentSubscriptionsStub(channel)),
                gossip=Gossip(GossipStub(channel)),
            )

    async def discover_endpoint(self) -> str:
        for attempt in range(1, self.discovery_attempts + 1):
            candidates = self.endpoints.copy()
            random.shuffle(candidates)
            logger.info("Starting discovery attempt %s on %s", attempt, ",".join(candidates))
            for candidate in candidates:
                async with self._create_channel(candidate) as chan:
                    gossip = Gossip(GossipStub(chan))
                    members = await gossip.get_members(self.gossip_timeout)
                    if pick := pick_node(self.node_preference, members):
                        assert pick.endpoint
                        endpoint = f"{pick.endpoint.address}:{pick.endpoint.port}"
                        logger.info(
                            "Discovered %s node at %s (Preference: %s)",
                            pick.state.name,
                            endpoint,
                            self.node_preference.name,
                        )
                        return endpoint

            await asyncio.sleep(self.discovery_interval)
        raise DiscoveryError(f"Discovery failed after {self.discovery_attempts} attempt(s)")
