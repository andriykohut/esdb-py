from __future__ import annotations

import enum
import json
from dataclasses import dataclass
from typing import Optional

from esdb.client.streams.base import ContentType
from esdb.generated.persistent_pb2 import CreateReq, ReadResp


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


@dataclass
class SubscriptionSettings:
    @dataclass
    class DurationType:
        class Type(enum.Enum):
            TICKS = "ticks"
            MS = "ms"

        type: Type
        value: int

    @enum.unique
    class ConsumerStrategy(enum.Enum):
        DISPATCH_TO_SINGLE = "DispatchToSingle"
        ROUND_ROBIN = "RoundRobin"
        PINNED = "Pinned"

    live_buffer_size: int
    read_batch_size: int
    history_buffer_size: int
    checkpoint: DurationType
    resolve_links: Optional[bool] = None
    extra_statistics: Optional[bool] = None
    max_retry_count: Optional[int] = None
    min_checkpoint_count: Optional[int] = None
    max_checkpoint_count: Optional[int] = None
    max_subscriber_count: Optional[int] = None
    message_timeout: Optional[DurationType] = None
    consumer_strategy: Optional[ConsumerStrategy] = None

    def to_protobuf(self) -> CreateReq.Settings:
        assert (
            self.read_batch_size < self.live_buffer_size
        ), "read_batch_size may not be greater than or equal to live_buffer_size"
        assert (
            self.read_batch_size < self.history_buffer_size
        ), "read_batch_size may not be greater than or equal to history_buffer_size"
        settings = CreateReq.Settings(
            resolve_links=self.resolve_links,
            extra_statistics=self.extra_statistics,
            max_retry_count=self.max_retry_count,
            min_checkpoint_count=self.min_checkpoint_count,
            max_checkpoint_count=self.max_checkpoint_count,
            max_subscriber_count=self.max_subscriber_count,
            live_buffer_size=self.live_buffer_size,
            read_batch_size=self.read_batch_size,
            history_buffer_size=self.history_buffer_size,
            consumer_strategy=self.consumer_strategy.value if self.consumer_strategy else None,
        )

        if self.checkpoint.type == self.DurationType.Type.MS:
            settings.checkpoint_after_ms = self.checkpoint.value
        elif self.checkpoint.type == self.DurationType.Type.TICKS:
            settings.checkpoint_after_ticks = self.checkpoint.value

        if self.message_timeout:
            if self.message_timeout.type == self.DurationType.Type.MS:
                settings.message_timeout_ms = self.message_timeout.value
            elif self.message_timeout.type == self.DurationType.Type.TICKS:
                settings.message_timeout_ticks = self.message_timeout.value

        return settings
