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
from typing import AsyncContextManager, Optional

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

    @classmethod
    def from_string(cls, s: str) -> Preference:
        return {
            "follower": cls.FOLLOWER,
            "leader": cls.LEADER,
            "readonlyreplica": cls.READ_ONLY_REPLICA,
        }[s.lower()]


@dataclass
class Configuration:
    address: Optional[Member.Endpoint] = None
    gossip_seed: Optional[list[Member.Endpoint]] = None
    username: Optional[str] = None
    password: Optional[str] = None
    disable_tls: bool = False
    node_preference: Preference = Preference.LEADER
    verify_cert: bool = True
    root_cert: Optional[bytes] = None
    max_discovery_attempts: int = 10
    discovery_interval: int = 100
    gossip_timeout: int = 5
    dns_discover: bool = False
    keep_alive_interval: int = 10
    keep_alive_timeout: int = 10
    default_deadline: int = 10


class BasicAuthPlugin(grpc.AuthMetadataPlugin):
    def __init__(self, user: str, password: str) -> None:
        self.__auth = base64.b64encode(f"{user}:{password}".encode())

    def __call__(self, _: grpc.AuthMetadataContext, callback: grpc.AuthMetadataPluginCallback) -> None:
        callback((("authorization", b"Basic " + self.__auth),), None)


@dataclass
class Connection:
    channel: grpc.aio._base_channel.Channel  # type: ignore
    streams: Streams
    subscriptions: PersistentSubscriptions
    gossip: Gossip
    config: Configuration


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


def parse_endpoint(s: str) -> Member.Endpoint:
    if ":" in s:
        items = s.split(":")
        if len(items) != 2:
            raise ValueError("Too many colons in a host")
        host, port_str = items
        try:
            port = int(port_str)
        except ValueError:
            raise ValueError(f"{port_str} port is not a number")
        return Member.Endpoint(host, port)

    return Member.Endpoint(s, 2113)


def parse_settings(query: str, c: Configuration) -> None:
    def _str_to_bool(s: str) -> bool:
        return {"true": True, "false": False}[s.lower()]

    for k, v in urllib.parse.parse_qs(query, strict_parsing=True).items():
        if len(v) != 1:
            raise ValueError(f"Too many values for {k}")
        key = k.lower()
        [val] = v
        if key == "discoveryinterval":
            c.discovery_interval = int(val)
        elif key == "gossiptimeout":
            c.gossip_timeout = int(val)
        elif key == "maxdiscoverattempts":
            c.max_discovery_attempts = int(val)
        elif key == "nodepreference":
            c.node_preference = Preference.from_string(val)
        elif key == "keepaliveinterval":
            c.keep_alive_interval = int(val)
        elif key == "keepalivetimeout":
            c.keep_alive_timeout = int(val)
        elif key == "tls":
            c.disable_tls = not _str_to_bool(val)
        elif key == "tlscafile":
            with open(val, "rb") as fh:
                c.root_cert = fh.read()
        elif key == "tlsverifycert":
            c.verify_cert = _str_to_bool(val)
        elif key == "defaultdeadline":
            c.default_deadline = int(val)
        else:
            raise ValueError(f"Invalid option {k}")


def parse_connection_string(connection_string: str) -> Configuration:
    config = Configuration()
    scheme, rest = connection_string.split("://")
    if scheme not in ("esdb", "esdb+discover"):
        raise ValueError("esdb:// or esdb+discover:// scheme is required")

    config.dns_discover = scheme == "esdb+discover"

    if "@" in rest:
        user_info, rest = rest.split("@")
        user_info_items = user_info.split(":")
        if len(user_info_items) != 2:
            raise ValueError("Invalid user credentials")
        user, password = user_info_items
        if not user:
            raise ValueError("Username is required")
        if not password:
            raise ValueError("Password is required")
        config.username, config.password = user, password

    hosts, *queries = rest.split("?")
    endpoints = []
    for host in hosts.split(","):
        endpoints.append(parse_endpoint(host))
    if len(endpoints) == 1:
        config.address = endpoints[0]
    else:
        config.gossip_seed = endpoints

    if queries:
        [settings_query] = queries
        parse_settings(settings_query, config)

    return config


class ESClient:
    def __init__(
        self,
        connection_string: str,
        root_certificates: Optional[bytes] = None,
        private_key: Optional[bytes] = None,
        certificate_chain: Optional[bytes] = None,
    ) -> None:
        self.config = parse_connection_string(connection_string)
        self.options = [
            ("grpc.keepalive_time_ms", self.config.keep_alive_interval * 1000),
            ("grpc.keepalive_timeout_ms", self.config.keep_alive_timeout * 1000),
        ]

        if not self.config.disable_tls:
            self.channel_credentials = grpc.ssl_channel_credentials(
                root_certificates=root_certificates or self.config.root_cert,
                private_key=private_key,
                certificate_chain=certificate_chain,
            )

        if self.config.username and self.config.password:
            self.call_credentials = grpc.metadata_call_credentials(
                BasicAuthPlugin(self.config.username, self.config.password), name="auth"
            )

    def _create_channel(self, endpoint: Member.Endpoint) -> grpc.aio.Channel:  # type: ignore
        if self.config.disable_tls:
            return grpc.aio.insecure_channel(  # type: ignore
                f"{endpoint.address}:{endpoint.port}", options=self.options
            )
        assert self.channel_credentials
        credentials = (
            grpc.composite_channel_credentials(self.channel_credentials, self.call_credentials)
            if self.call_credentials
            else self.channel_credentials
        )
        return grpc.aio.secure_channel(  # type: ignore
            f"{endpoint.address}:{endpoint.port}", credentials, self.options
        )

    @contextlib.asynccontextmanager  # type: ignore
    async def connect(self) -> AsyncContextManager[Connection]:  # type: ignore
        if self.config.dns_discover:
            endpoint = await self.discover_endpoint()
        else:
            assert self.config.address
            endpoint = self.config.address

        async with self._create_channel(endpoint) as channel:
            yield Connection(
                channel=channel,
                streams=Streams(StreamsStub(channel)),
                subscriptions=PersistentSubscriptions(PersistentSubscriptionsStub(channel)),
                gossip=Gossip(GossipStub(channel)),
                config=self.config,
            )

    async def discover_endpoint(self) -> Member.Endpoint:
        for attempt in range(1, self.config.max_discovery_attempts + 1):
            candidates = (
                self.config.gossip_seed.copy() if self.config.gossip_seed else [self.config.address]  # type: ignore
            )
            random.shuffle(candidates)
            logger.info(
                "Starting discovery attempt %s on %s", attempt, ",".join(f"{c.address}:{c.port}" for c in candidates)
            )
            for candidate in candidates:
                async with self._create_channel(candidate) as chan:
                    gossip = Gossip(GossipStub(chan))
                    members = await gossip.get_members(self.config.gossip_timeout)
                    if pick := pick_node(self.config.node_preference, members):
                        assert pick.endpoint
                        logger.info(
                            "Discovered %s node at %s (Preference: %s)",
                            pick.state.name,
                            f"{pick.endpoint.address}:{pick.endpoint.port}",
                            self.config.node_preference.name,
                        )
                        return pick.endpoint

            await asyncio.sleep(self.config.discovery_interval)
        raise DiscoveryError(f"Discovery failed after {self.config.max_discovery_attempts} attempt(s)")
