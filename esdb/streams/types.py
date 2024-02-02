from __future__ import annotations

import enum
import json
import logging
import uuid
from dataclasses import dataclass, field
from typing import Mapping, Optional, Type, TypeVar, Union

from esdb.generated.shared_pb2 import UUID
from esdb.generated.streams_pb2 import (
    AppendReq,
    AppendResp,
    BatchAppendReq,
    BatchAppendResp,
    DeleteResp,
    ReadResp,
    TombstoneResp,
)

logger = logging.getLogger(__name__)


@enum.unique
class StreamState(enum.Enum):
    ANY = "any"
    NO_STREAM = "no_stream"
    STREAM_EXISTS = "stream_exists"


@dataclass
class AppendResult:
    current_revision: int
    commit_position: int
    prepare_position: int

    @staticmethod
    def from_response(response: AppendResp) -> AppendResult:
        return AppendResult(
            current_revision=response.success.current_revision,
            commit_position=response.success.position.commit_position,
            prepare_position=response.success.position.prepare_position,
        )


@dataclass
class DeleteResult:
    commit_position: int
    prepare_position: int

    @staticmethod
    def from_response(response: DeleteResp) -> DeleteResult:
        return DeleteResult(
            commit_position=response.position.commit_position,
            prepare_position=response.position.prepare_position,
        )


@dataclass
class TombstoneResult:
    commit_position: int
    prepare_position: int

    @staticmethod
    def from_response(response: TombstoneResp) -> TombstoneResult:
        return TombstoneResult(
            commit_position=response.position.commit_position,
            prepare_position=response.position.prepare_position,
        )


@enum.unique
class ContentType(enum.Enum):
    OCTET_STREAM = "application/octet-stream"
    JSON = "application/json"


@dataclass
class ReadEvent:
    id: str
    stream_name: str
    prepare_position: int
    commit_position: int
    metadata: Mapping[str, str]
    event_type: str
    custom_metadata: Optional[dict]
    data: Union[dict, bytes]

    @staticmethod
    def from_response(response: ReadResp) -> ReadEvent:
        return ReadEvent(
            id=response.event.event.id.string,
            stream_name=response.event.event.stream_identifier.stream_name.decode(),
            metadata=response.event.event.metadata,
            custom_metadata=(
                json.loads(response.event.event.custom_metadata) if response.event.event.custom_metadata else None
            ),
            data=(
                json.loads(response.event.event.data)
                if response.event.event.metadata["content-type"] == ContentType.JSON.value
                else response.event.event.data
            ),
            prepare_position=response.event.commit_position,
            commit_position=response.event.commit_position,
            event_type=response.event.event.metadata["type"],
        )


@dataclass
class SubscriptionConfirmed:
    subscription_id: str


@dataclass
class Checkpoint:
    commit_position: int
    prepare_position: int


ProposedMessageType = TypeVar("ProposedMessageType", BatchAppendReq.ProposedMessage, AppendReq.ProposedMessage)


@dataclass
class Message:
    event_type: str
    data: Union[bytes, dict]
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    custom_metadata: Optional[dict] = None

    def to_protobuf(self, message_type: Type[ProposedMessageType]) -> ProposedMessageType:
        assert isinstance(self.data, (bytes, dict))
        return message_type(
            id=UUID(string=str(self.id)),
            metadata={
                "type": self.event_type,
                "content-type": (
                    ContentType.OCTET_STREAM.value if isinstance(self.data, bytes) else ContentType.JSON.value
                ),
            },
            custom_metadata=json.dumps(self.custom_metadata).encode() if self.custom_metadata else b"",
            data=json.dumps(self.data).encode() if isinstance(self.data, dict) else self.data,
        )


@dataclass
class BatchAppendResult:
    correlation_id: str
    current_revision: int
    commit_position: int
    prepare_position: int

    @staticmethod
    def from_response(response: BatchAppendResp) -> BatchAppendResult:
        return BatchAppendResult(
            correlation_id=response.correlation_id,
            current_revision=response.success.current_revision,
            commit_position=response.success.position.commit_position,
            prepare_position=response.success.position.prepare_position,
        )
