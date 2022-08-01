from __future__ import annotations

import asyncio
from typing import AsyncIterable, AsyncIterator, Optional

from esdb.generated.persistent_pb2 import CreateReq, CreateResp, ReadReq, ReadResp
from esdb.generated.persistent_pb2_grpc import PersistentSubscriptionsStub
from esdb.generated.shared_pb2 import UUID, Empty, StreamIdentifier
from esdb.shared import Filter
from esdb.subscriptions.types import Event, NackAction, SubscriptionSettings


class Subscription:
    def __init__(
        self, group_name: str, buffer_size: int, stream: Optional[str], stub: PersistentSubscriptionsStub
    ) -> None:
        self.stream = stream
        self.group_name = group_name
        self.buffer_size = buffer_size
        self.send_queue: asyncio.Queue = asyncio.Queue()
        self.stub = stub
        self.subscription_id: Optional[str] = None

    async def __aiter__(self) -> AsyncIterable[Event]:
        read_request = ReadReq(
            options=ReadReq.Options(
                stream_identifier=StreamIdentifier(stream_name=self.stream.encode()) if self.stream else None,
                all=Empty() if self.stream is None else None,
                group_name=self.group_name,
                buffer_size=self.buffer_size,
                uuid_option=ReadReq.Options.UUIDOption(structured=Empty(), string=Empty()),
            ),
            ack=None,
            nack=None,
        )
        await self.send_queue.put(read_request)

        async def queue_iter():
            while True:
                yield await self.send_queue.get()
                self.send_queue.task_done()

        reader: AsyncIterator[ReadResp] = self.stub.Read(queue_iter())
        async for response in reader:
            if not self.subscription_id and response.WhichOneof("content") == "subscription_confirmation":
                self.subscription_id = response.subscription_confirmation.subscription_id
                continue
            yield Event.from_read_response_event(response.event)

    async def ack(self, events: list[Event]) -> None:
        assert self.subscription_id, "Nothing to ack, not reading from a subscription yet"
        await self.send_queue.put(
            ReadReq(
                ack=ReadReq.Ack(
                    id=self.subscription_id.encode(),
                    ids=(UUID(string=evt.id) for evt in events),
                )
            )
        )

    async def nack(self, events: list[Event], action: NackAction, reason: Optional[str] = None) -> None:
        assert self.subscription_id, "Nothing to nack, not reading from a subscription yet"
        await self.send_queue.put(
            ReadReq(
                nack=ReadReq.Nack(
                    id=self.subscription_id.encode(),
                    ids=(UUID(string=evt.id) for evt in events),
                    action=action.value,
                    reason=reason or "",
                )
            )
        )


class PersistentSubscriptions:
    def __init__(self, stub: PersistentSubscriptionsStub) -> None:
        self._stub = stub

    async def create_stream_subscription(
        self, stream: str, group_name: str, settings: SubscriptionSettings, backwards: bool = False
    ) -> None:
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
                settings=settings.to_protobuf(),
            )
        )
        response: CreateResp = await self._stub.Create(create_request)
        assert isinstance(response, CreateResp), f"Expected {CreateResp} got {response.__class__}"

    async def create_all_subscription(
        self,
        group_name: str,
        settings: SubscriptionSettings,
        backwards: bool = False,
        filter_by: Optional[Filter] = None,
    ) -> None:
        create_request = CreateReq(
            options=CreateReq.Options(
                group_name=group_name,
                settings=settings.to_protobuf(),
                all=CreateReq.AllOptions(
                    # position=CreateReq.Position(), TODO: deal with position
                    start=None if backwards else Empty(),
                    end=Empty() if backwards else None,
                    no_filter=Empty() if filter_by is None else None,
                    filter=filter_by.to_protobuf(CreateReq.AllOptions.FilterOptions) if filter_by else None,
                ),
            )
        )
        response: CreateResp = await self._stub.Create(create_request)
        assert isinstance(response, CreateResp), f"Expected {CreateResp} got {response.__class__}"

    def subscribe(
        self,
        group_name: str,
        buffer_size: int,
        stream: Optional[str] = None,
    ) -> Subscription:
        return Subscription(stream=stream, group_name=group_name, buffer_size=buffer_size, stub=self._stub)
