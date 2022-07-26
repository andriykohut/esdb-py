import grpc

from streams import Streams
from streams_pb2_grpc import StreamsStub


class ESClient:
    def __init__(self, target: str) -> None:
        self.__channel = grpc.insecure_channel(target)
        self.streams = Streams(StreamsStub(self.__channel))
