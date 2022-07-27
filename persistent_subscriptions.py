from typing import Callable, Optional

from grpc._channel import _MultiThreadedRendezvous

from persistent_pb2 import CreateReq, CreateResp, ReadReq, ReadResp
from persistent_pb2_grpc import PersistentSubscriptionsStub
from shared_pb2 import Empty, StreamIdentifier


class PersistentSubscriptions:
    def __init__(self, stub: PersistentSubscriptionsStub) -> None:
        self._stub = stub

    def create_stream_subscription(self, stream: str, group_name: str, revision: int, backwards: bool = False) -> None:
        stream_identifier = StreamIdentifier(stream_name=stream.encode())
        create_request = CreateReq(
            options=CreateReq.Options(
                stream=CreateReq.StreamOptions(
                    stream_identifier=stream_identifier,
                    revision=revision,
                    start=None if backwards else Empty(),
                    end=Empty() if backwards else None,
                ),
                stream_identifier=stream_identifier,
                group_name=group_name,
                settings=CreateReq.Settings(
                    # revision=revision,
                    # max_retry_count=2,
                    # min_checkpoint_count=1,
                    # max_checkpoint_count=1,
                    # max_subscriber_count=5,
                    # extra_statistics=False,
                    # resolve_links=True,
                    consumer_strategy="RoundRobin",  # TODO,
                    read_batch_size=9,
                    live_buffer_size=10,
                    history_buffer_size=10,
                    # message_timeout_ticks=100,
                    # message_timeout_ms=1000,
                    # checkpoint_after_ticks=1,
                    # checkpoint_after_ms=1,
                ),
            )
        )
        response: CreateResp = self._stub.Create(create_request)
        assert isinstance(response, CreateResp)

    def subscribe_to_stream(
        self,
        stream: str,
        group_name: str,
        handler: Callable[[ReadResp, _MultiThreadedRendezvous], None],
        buffer_size: int = 10,
    ) -> "TODO":
        read_request = ReadReq(
            options=ReadReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                all=None,
                group_name=group_name,
                buffer_size=10,
                uuid_option=ReadReq.Options.UUIDOption(structured=Empty(), string=Empty()),
            ),
            ack=None,
            nack=None,
        )

        reader = self._stub.Read(iter([read_request]))

        for response in reader:
            handler(response, reader)
