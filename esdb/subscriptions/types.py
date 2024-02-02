from __future__ import annotations

import enum
import json
from dataclasses import dataclass
from typing import Mapping, Optional, Type, TypeVar, Union

from esdb.generated.persistent_pb2 import CreateReq, ReadReq, ReadResp
from esdb.generated.persistent_pb2 import SubscriptionInfo as SubscriptionInfoPB
from esdb.generated.persistent_pb2 import UpdateReq
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
            data=(
                json.loads(event.event.data)
                if event.event.metadata["content-type"] == ContentType.JSON.value
                else event.event.data
            ),
        )


SettingsType = TypeVar("SettingsType", CreateReq.Settings, UpdateReq.Settings)


@dataclass
class SubscriptionSettings:
    class ConsumerStrategy(enum.Enum):
        DISPATCH_TO_SINGLE = "DispatchToSingle"
        ROUND_ROBIN = "RoundRobin"
        PINNED = "Pinned"

    live_buffer_size: int
    read_batch_size: int
    history_buffer_size: int
    checkpoint_ms: int
    resolve_links: Optional[bool] = None
    extra_statistics: Optional[bool] = None
    max_retry_count: Optional[int] = None
    min_checkpoint_count: Optional[int] = None
    max_checkpoint_count: Optional[int] = None
    max_subscriber_count: Optional[int] = None
    message_timeout_ms: Optional[int] = None
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
            else:
                settings.named_consumer_strategy = {  # type: ignore
                    self.ConsumerStrategy.DISPATCH_TO_SINGLE: 0,
                    self.ConsumerStrategy.ROUND_ROBIN: 1,
                    self.ConsumerStrategy.PINNED: 2,
                }[self.consumer_strategy]

        settings.checkpoint_after_ms = self.checkpoint_ms

        if self.message_timeout_ms:
            settings.message_timeout_ms = self.message_timeout_ms

        return settings


class NackAction(enum.Enum):
    UNKNOWN = ReadReq.Nack.Action.Unknown
    PARK = ReadReq.Nack.Action.Park
    RETRY = ReadReq.Nack.Action.Retry
    SKIP = ReadReq.Nack.Action.Skip
    STOP = ReadReq.Nack.Action.Stop


@dataclass
class ConnectionInfo:
    username: str
    average_items_per_second: int
    total_items: int
    count_since_last_measurement: int
    observed_measurements: dict[str, int]
    available_slots: int
    in_flight_messages: int
    connection_name: str

    @classmethod
    def from_protobuf(cls, info: SubscriptionInfoPB.ConnectionInfo) -> ConnectionInfo:
        return cls(
            username=info.username,
            average_items_per_second=info.average_items_per_second,
            total_items=info.total_items,
            count_since_last_measurement=info.count_since_last_measurement,
            observed_measurements={m.key: m.value for m in info.observed_measurements},
            available_slots=info.available_slots,
            in_flight_messages=info.in_flight_messages,
            connection_name=info.connection_name,
        )


@dataclass
class SubscriptionInfo:
    event_source: str
    group_name: str
    status: str
    connections: list[ConnectionInfo]
    average_per_second: int
    total_items: int
    count_since_last_measurement: int
    last_checkpointed_event_position: str
    last_known_event_position: str
    resolve_link_tos: bool
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
    read_buffer_count: int
    live_buffer_count: int
    retry_buffer_count: int
    total_in_flight_messages: int
    outstanding_messages_count: int
    consumer_strategy: str
    max_subscriber_count: int
    parked_message_count: int

    @classmethod
    def from_protobuf(cls, info: SubscriptionInfoPB) -> SubscriptionInfo:
        return cls(
            event_source=info.event_source,
            group_name=info.group_name,
            status=info.status,
            connections=[ConnectionInfo.from_protobuf(c) for c in info.connections],
            start_from=info.start_from,
            message_timeout_milliseconds=info.message_timeout_milliseconds,
            extra_statistics=info.extra_statistics,
            max_retry_count=info.max_retry_count,
            live_buffer_size=info.live_buffer_size,
            buffer_size=info.buffer_size,
            read_batch_size=info.read_batch_size,
            check_point_after_milliseconds=info.check_point_after_milliseconds,
            min_check_point_count=info.min_check_point_count,
            max_check_point_count=info.max_check_point_count,
            consumer_strategy=info.named_consumer_strategy,
            max_subscriber_count=info.max_subscriber_count,
            average_per_second=info.average_per_second,
            count_since_last_measurement=info.count_since_last_measurement,
            last_checkpointed_event_position=info.last_checkpointed_event_position,
            last_known_event_position=info.last_known_event_position,
            live_buffer_count=info.live_buffer_count,
            outstanding_messages_count=info.outstanding_messages_count,
            parked_message_count=info.parked_message_count,
            read_buffer_count=info.read_buffer_count,
            resolve_link_tos=info.resolve_link_tos,
            retry_buffer_count=info.retry_buffer_count,
            total_in_flight_messages=info.total_in_flight_messages,
            total_items=info.total_items,
        )
