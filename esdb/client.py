from __future__ import annotations

import base64
import contextlib
import logging
from dataclasses import dataclass
from typing import AsyncContextManager, Optional

import grpc

from esdb.generated.gossip_pb2_grpc import GossipStub
from esdb.generated.persistent_pb2_grpc import PersistentSubscriptionsStub
from esdb.generated.streams_pb2_grpc import StreamsStub
from esdb.gossip import Gossip, State
from esdb.streams import Streams
from esdb.subscriptions import PersistentSubscriptions

logger = logging.getLogger(__name__)


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


class ESClient:
    def __init__(
        self,
        target: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        insecure: bool = False,
        root_certificates: Optional[bytes] = None,
        private_key: Optional[bytes] = None,
        certificate_chain: Optional[bytes] = None,
        keepalive_time_ms: int = 10000,
        keepalive_timeout_ms: int = 10000,
        discover: bool = False,
    ) -> None:
        self.channel_credentials = None
        self.call_credentials = None
        self.insecure = insecure
        self.target = target
        self.discover = discover

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

    def _channel_builder(self, target: str) -> grpc.aio.Channel:  # type: ignore
        if self.insecure:
            return grpc.aio.insecure_channel(target, options=self.options)  # type: ignore
        assert self.channel_credentials
        credentials = (
            grpc.composite_channel_credentials(self.channel_credentials, self.call_credentials)
            if self.call_credentials
            else self.channel_credentials
        )
        return grpc.aio.secure_channel(target, credentials, self.options)  # type: ignore

    @contextlib.asynccontextmanager  # type: ignore
    async def connect(self) -> AsyncContextManager[Connection]:  # type: ignore
        target = self.target
        if self.discover:
            # TODO: handle preferences
            async with self._channel_builder(self.target) as channel:
                logger.debug("Starting discovery from %s", self.target)
                gossip = Gossip(GossipStub(channel))
                members = await gossip.get_members()
                leader = next(m for m in members if m.state == State.Leader)
                logger.debug("Discovered a leader: %s:%s", leader.endpoint.address, leader.endpoint.port)
                target = f"{leader.endpoint.address}:{leader.endpoint.port}"

        async with self._channel_builder(target) as channel:
            yield Connection(
                channel=channel,
                streams=Streams(StreamsStub(channel)),
                subscriptions=PersistentSubscriptions(PersistentSubscriptionsStub(channel)),
                gossip=Gossip(GossipStub(channel)),
            )
