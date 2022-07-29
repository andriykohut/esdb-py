from __future__ import annotations

import base64
import contextlib
from dataclasses import dataclass
from typing import AsyncContextManager, ContextManager, Optional

import grpc

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
        credentials = None
        channel_credentials = None
        call_credentials = None

        options = [
            ("grpc.keepalive_time_ms", keepalive_time_ms),
            ("grpc.keepalive_timeout_ms", keepalive_timeout_ms),
        ]

        if tls:
            if not root_certificates:
                raise ValueError("root_certificates is required for TLS")
            channel_credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates)

        if any([username, password]) and not all([username, password]):
            raise ValueError("Both username and password are required")

        if username and password:
            call_credentials = grpc.metadata_call_credentials(BasicAuthPlugin(username, password), name="auth")

        channel_func = grpc.secure_channel if tls else grpc.insecure_channel

        if channel_credentials and call_credentials:
            credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
        elif channel_credentials:
            credentials = channel_credentials
        elif call_credentials:
            credentials = call_credentials
        self.__channel_builder = (
            lambda: channel_func(target, credentials, options=options)
            if credentials
            else channel_func(target, options=options)
        )

    @contextlib.contextmanager
    def connect(self) -> ContextManager[Connection]:
        with self.__channel_builder() as channel:
            yield Connection(
                channel=channel,
                streams=Streams(StreamsStub(channel)),
                subscriptions=PersistentSubscriptions(PersistentSubscriptionsStub(channel)),
            )


@dataclass
class AsyncConnection:
    channel: grpc.aio._base_channel.Channel
    streams: StreamsAsync
    subscriptions: PersistentSubscriptionsAsync


class AsyncESClient:
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
        credentials = None
        channel_credentials = None
        call_credentials = None
        options = [
            ("grpc.keepalive_time_ms", keepalive_time_ms),
            ("grpc.keepalive_timeout_ms", keepalive_timeout_ms),
        ]

        if tls:
            if not root_certificates:
                raise ValueError("root_certificates is required for TLS")
            channel_credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates)

        if any([username, password]) and not all([username, password]):
            raise ValueError("Both username and password are required")

        if username and password:
            call_credentials = grpc.metadata_call_credentials(BasicAuthPlugin(username, password), name="auth")

        channel_func = grpc.aio.secure_channel if tls else grpc.aio.insecure_channel

        if channel_credentials and call_credentials:
            credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
        elif channel_credentials:
            credentials = channel_credentials
        elif call_credentials:
            credentials = call_credentials

        self.__channel_builder = (
            lambda: channel_func(target, credentials, options=options)
            if credentials
            else channel_func(target, options=options)
        )

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncContextManager[AsyncConnection]:
        async with self.__channel_builder() as channel:
            yield AsyncConnection(
                channel=channel,
                streams=StreamsAsync(StreamsStub(channel)),
                subscriptions=PersistentSubscriptionsAsync(PersistentSubscriptionsStub(channel)),
            )
