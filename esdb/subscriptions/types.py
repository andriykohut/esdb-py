from __future__ import annotations

import enum
import json
from dataclasses import dataclass
from typing import Mapping, Optional, Type, TypeVar, Union

from esdb.generated.persistent_pb2 import CreateReq, ReadReq, ReadResp, UpdateReq
from esdb.streams.types import ContentType


@dataclass
class Event:
    id: str
    retry_count: int
    stream: str
    prepare_position: int
    commit_position: int
    metadata: Mapping[str, str]
    type: str
    data: Union[bytes, dict]

    @staticmethod
    def from_read_response_event(event: ReadResp.ReadEvent) -> Event:
        return Event(
            id=event.event.id.string,
            retry_count=event.retry_count,
            stream=event.event.stream_identifier.stream_name.decode(),
            prepare_position=event.event.prepare_position,
            commit_position=event.event.commit_position,
            metadata=event.event.metadata,
            type=event.event.metadata["type"],
            data=json.loads(event.event.data)
            if event.event.metadata["content-type"] == ContentType.JSON.value
            else event.event.data,
        )


SettingsType = TypeVar("SettingsType", CreateReq.Settings, UpdateReq.Settings)


@dataclass
class SubscriptionSettings:
    @dataclass
    class DurationType:
        class Type(enum.Enum):
            TICKS = "ticks"
            MS = "ms"

        type: Type
        value: int

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

    def to_protobuf(self, cls: Type[SettingsType]) -> SettingsType:
        assert (
            self.read_batch_size < self.live_buffer_size
        ), "read_batch_size may not be greater than or equal to live_buffer_size"
        assert (
            self.read_batch_size < self.history_buffer_size
        ), "read_batch_size may not be greater than or equal to history_buffer_size"
        settings = cls(
            live_buffer_size=self.live_buffer_size,
            read_batch_size=self.read_batch_size,
            history_buffer_size=self.history_buffer_size,
        )

        if self.resolve_links is not None:
            settings.resolve_links = self.resolve_links
        if self.extra_statistics is not None:
            settings.extra_statistics = self.extra_statistics
        if self.max_retry_count is not None:
            settings.max_retry_count = self.max_retry_count
        if self.min_checkpoint_count is not None:
            settings.min_checkpoint_count = self.min_checkpoint_count
        if self.max_checkpoint_count is not None:
            settings.max_checkpoint_count = self.max_checkpoint_count
        if self.max_subscriber_count is not None:
            settings.max_subscriber_count = self.max_subscriber_count
        if self.consumer_strategy:
            if cls is CreateReq.Settings:
                settings.consumer_strategy = self.consumer_strategy.value  # type: ignore
            elif cls is UpdateReq.Settings:
                settings.named_consumer_strategy = {  # type: ignore
                    self.ConsumerStrategy.DISPATCH_TO_SINGLE: 0,
                    self.ConsumerStrategy.ROUND_ROBIN: 1,
                    self.ConsumerStrategy.PINNED: 2,
                }[self.consumer_strategy]

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


class NackAction(enum.Enum):
    UNKNOWN = ReadReq.Nack.Action.Unknown
    PARK = ReadReq.Nack.Action.Park
    RETRY = ReadReq.Nack.Action.Retry
    SKIP = ReadReq.Nack.Action.Skip
    STOP = ReadReq.Nack.Action.Stop


@dataclass
class SubscriptionInfo:
    group_name: str
    status: str
    start_from: str
    message_timeout_milliseconds: int
    extra_statistics: bool
    max_retry_count: int
    live_buffer_size: int
    buffer_size: int
    read_batch_size: int
    check_point_after_milliseconds: int
    min_check_point_count: int
    max_check_point_count: int
    consumer_strategy: str
    max_subscriber_count: int
