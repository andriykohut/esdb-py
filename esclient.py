from __future__ import annotations
import grpc

from streams import Streams
from streams_async import Streams as StreamsAsync
from streams_pb2_grpc import StreamsStub


class ESClient:
    def __init__(self, target: str) -> None:
        self.__channel = grpc.insecure_channel(target)
        self.streams = Streams(StreamsStub(self.__channel))


class AsyncESClient:
    def __init__(self, target: str) -> None:
        self.__channel = grpc.aio.insecure_channel(target)
        self.streams = StreamsAsync(StreamsStub(self.__channel))