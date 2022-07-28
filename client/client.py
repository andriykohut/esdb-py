from __future__ import annotations

import abc
import base64
from contextlib import contextmanager
from typing import Optional

import grpc

from client.persistent_subscriptions import PersistentSubscriptions
from client.streams.aio import Streams as StreamsAsync
from client.streams.streams import Streams
from persistent_pb2_grpc import PersistentSubscriptionsStub
from streams_pb2_grpc import StreamsStub


class BasicAuthPlugin(grpc.AuthMetadataPlugin):
    def __init__(self, user: str, password: str) -> None:
        self.__auth = base64.b64encode(f"{user}:{password}".encode())

    def __call__(self, context, callback):
        callback((("authorization", b"Basic " + self.__auth),), None)


class BaseClient(abc.ABC):
    streams: Streams | StreamsAsync
    subscriptions: PersistentSubscriptions


class ESClient(BaseClient):
    def __init__(
        self,
        target: str,
        tls: bool = True,
        username: Optional[str] = None,
        password: Optional[str] = None,
        root_certificates: Optional[bytes] = None,
    ) -> None:
        credentials = None
        channel_credentials = None
        call_credentials = None

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

        self.__channel = channel_func(target, credentials) if credentials else channel_func(target)
        self.__channel_builder = lambda: channel_func(target, credentials) if credentials else channel_func(target)
        self.streams = Streams(StreamsStub(self.__channel))
        self.subscriptions = PersistentSubscriptions(PersistentSubscriptionsStub(self.__channel))

    @contextmanager
    def streams_channel(self):
        with self.__channel_builder() as channel:
            self.streams = Streams(StreamsStub(self.__channel))
            yield self


class AsyncESClient(BaseClient):
    def __init__(
        self,
        target: str,
        tls: bool = True,
        username: Optional[str] = None,
        password: Optional[str] = None,
        root_certificates: Optional[bytes] = None,
    ) -> None:
        credentials = None
        channel_credentials = None
        call_credentials = None

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

        self.__channel = channel_func(target, credentials) if credentials else channel_func(target)
        self.streams = StreamsAsync(StreamsStub(self.__channel))
