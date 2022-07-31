from __future__ import annotations

import base64
import contextlib
from dataclasses import dataclass
from typing import AsyncIterator, Optional

import grpc
from black import Iterator

from esdb.client.streams.aio import Streams as StreamsAsync
from esdb.client.streams.streams import Streams
from esdb.client.subscriptions.aio.subscriptions import (
    PersistentSubscriptions as PersistentSubscriptionsAsync,
)
from esdb.client.subscriptions.subscriptions import PersistentSubscriptions
from esdb.generated.persistent_pb2_grpc import PersistentSubscriptionsStub
from esdb.generated.streams_pb2_grpc import StreamsStub


class BasicAuthPlugin(grpc.AuthMetadataPlugin):
    def __init__(self, user: str, password: str) -> None:
        self.__auth = base64.b64encode(f"{user}:{password}".encode())

    def __call__(self, context, callback):
        callback((("authorization", b"Basic " + self.__auth),), None)


@dataclass
class Connection:
    channel: grpc.Channel
    streams: Streams
    subscriptions: PersistentSubscriptions


class ESClient:
    def __init__(
        self,
        target: str,
        tls: bool = True,
        username: Optional[str] = None,
        password: Optional[str] = None,
        root_certificates: Optional[bytes] = None,
        keepalive_time_ms: int = 10000,
        keepalive_timeout_ms: int = 10000,
    ) -> None:
        self.channel_credentials = None
        self.call_credentials = None
        self.tls = tls
        self.target = target

        self.options = [
            ("grpc.keepalive_time_ms", keepalive_time_ms),
            ("grpc.keepalive_timeout_ms", keepalive_timeout_ms),
        ]

        if tls:
            self.channel_credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates)

        if any([username, password]) and not all([username, password]):
            raise ValueError("Both username and password are required")

        if username and password:
            self.call_credentials = grpc.metadata_call_credentials(BasicAuthPlugin(username, password), name="auth")

    def _channel_builder(self) -> grpc.Channel:
        if not self.tls:
            return grpc.insecure_channel(self.target, options=self.options)
        assert self.channel_credentials
        credentials = (
            grpc.composite_channel_credentials(self.channel_credentials, self.call_credentials)
            if self.call_credentials
            else self.channel_credentials
        )
        return grpc.secure_channel(self.target, credentials, self.options)

    @contextlib.contextmanager
    def connect(self) -> Iterator[Connection]:
        with self._channel_builder() as channel:
            yield Connection(
                channel=channel,
                streams=Streams(StreamsStub(channel)),
                subscriptions=PersistentSubscriptions(PersistentSubscriptionsStub(channel)),
            )


@dataclass
class AsyncConnection:
    channel: grpc.aio._base_channel.Channel  # type: ignore
    streams: StreamsAsync
    subscriptions: PersistentSubscriptionsAsync


class AsyncESClient(ESClient):
    def _channel_builder(self) -> grpc.aio.Channel:  # type: ignore
        if not self.tls:
            return grpc.aio.insecure_channel(self.target, options=self.options)  # type: ignore
        assert self.channel_credentials
        credentials = (
            grpc.composite_channel_credentials(self.channel_credentials, self.call_credentials)
            if self.call_credentials
            else self.channel_credentials
        )
        return grpc.aio.secure_channel(self.target, credentials, self.options)  # type: ignore

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:  # type: ignore
        async with self._channel_builder() as channel:
            yield AsyncConnection(
                channel=channel,
                streams=StreamsAsync(StreamsStub(channel)),
                subscriptions=PersistentSubscriptionsAsync(PersistentSubscriptionsStub(channel)),
            )
