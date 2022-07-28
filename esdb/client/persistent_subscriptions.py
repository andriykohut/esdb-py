from __future__ import annotations

import json
import queue
from dataclasses import dataclass
from typing import Iterable, Optional

from esdb.client.streams.base import ContentType
from esdb.generated.persistent_pb2 import CreateReq, CreateResp, ReadReq, ReadResp
from esdb.generated.persistent_pb2_grpc import PersistentSubscriptionsStub
from esdb.generated.shared_pb2 import UUID, Empty, StreamIdentifier


@dataclass
class Event:
    id: str
    retry_count: int
    stream: str
    prepare_position: int
    commit_position: int
    metadata: dict
    type: str
    data: bytes | dict

    @staticmethod
    def from_read_response(response: ReadResp) -> Event:
        return Event(
            id=response.event.event.id.string,
            retry_count=response.event.retry_count,
            stream=response.event.event.stream_identifier.stream_name.decode(),
            prepare_position=response.event.event.prepare_position,
            commit_position=response.event.event.commit_position,
            metadata=response.event.event.metadata,
            type=response.event.event.metadata["type"],
            data=json.loads(response.event.event.data)
            if response.event.event.metadata["content-type"] == ContentType.JSON
            else response.event.event.data,
        )


class SubscriptionStream:
    def __init__(self, stream: str, group_name: str, buffer_size: int, stub: PersistentSubscriptionsStub) -> None:
        self.stream = stream
        self.group_name = group_name
        self.buffer_size = buffer_size
        self.send_queue = queue.SimpleQueue()
        self.stub = stub
        self.subscription_id: Optional[str] = None

    def __iter__(self) -> Iterable[Event]:
        read_request = ReadReq(
            options=ReadReq.Options(
                stream_identifier=StreamIdentifier(stream_name=self.stream.encode()),
                all=None,
                group_name=self.group_name,
                buffer_size=self.buffer_size,
                uuid_option=ReadReq.Options.UUIDOption(structured=Empty(), string=Empty()),
            ),
            ack=None,
            nack=None,
        )
        self.send_queue.put(read_request)
        reader: Iterable[ReadResp] = self.stub.Read(iter(self.send_queue.get, None))
        confirmation: ReadResp = next(reader)
        self.subscription_id = confirmation.subscription_confirmation.subscription_id
        for event in reader:
            yield Event.from_read_response(event)

    def ack(self, events: list[Event]) -> None:
        assert self.subscription_id, "Nothing to ack, not reading from a subscription yet"
        self.send_queue.put(
            ReadReq(
                ack=ReadReq.Ack(
                    id=self.subscription_id.encode(),
                    ids=(UUID(string=evt.id) for evt in events),
                )
            )
        )


class PersistentSubscriptions:
    def __init__(self, stub: PersistentSubscriptionsStub) -> None:
        self._stub = stub

    def create_stream_subscription(self, stream: str, group_name: str, backwards: bool = False) -> None:
        stream_identifier = StreamIdentifier(stream_name=stream.encode())
        create_request = CreateReq(
            options=CreateReq.Options(
                stream=CreateReq.StreamOptions(
                    stream_identifier=stream_identifier,
                    start=None if backwards else Empty(),
                    end=Empty() if backwards else None,
                ),
                stream_identifier=stream_identifier,
                group_name=group_name,
                settings=CreateReq.Settings(
                    # max_retry_count=2,
                    # min_checkpoint_count=1,
                    # max_checkpoint_count=1,
                    # max_subscriber_count=5,
                    # extra_statistics=False,
                    resolve_links=True,
                    consumer_strategy="RoundRobin",  # TODO,
                    read_batch_size=2,
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
        buffer_size: int = 10,
    ) -> SubscriptionStream:
        return SubscriptionStream(stream=stream, group_name=group_name, buffer_size=buffer_size, stub=self._stub)
