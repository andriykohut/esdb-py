from __future__ import annotations

import abc
import enum
import json
import uuid
from dataclasses import dataclass, field
from typing import Iterable, Optional, Type, TypeVar

from google.protobuf.duration_pb2 import Duration
from google.protobuf.empty_pb2 import Empty as GEmpty

from esdb.generated.shared_pb2 import UUID, Empty, StreamIdentifier
from esdb.generated.streams_pb2 import (
    AppendReq,
    AppendResp,
    BatchAppendReq,
    BatchAppendResp,
    DeleteReq,
    DeleteResp,
    ReadReq,
    ReadResp,
    TombstoneReq,
    TombstoneResp,
)
from esdb.generated.streams_pb2_grpc import StreamsStub


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
class ReadResult:
    id: str
    stream_name: str
    prepare_position: int
    commit_position: int
    metadata: dict
    event_type: str
    custom_metadata: dict | None
    data: dict | bytes

    @staticmethod
    def from_response(response: ReadResp) -> "ReadResult":
        return ReadResult(
            id=response.event.event.id.string,
            stream_name=response.event.event.stream_identifier.stream_name.decode(),
            metadata=response.event.event.metadata,
            custom_metadata=json.loads(response.event.event.custom_metadata)
            if response.event.event.custom_metadata
            else None,
            data=json.loads(response.event.event.data)
            if response.event.event.metadata["content-type"] == ContentType.JSON.value
            else response.event.event.data,
            prepare_position=response.event.commit_position,
            commit_position=response.event.commit_position,
            event_type=response.event.event.metadata["type"],
        )


ProposedMessageType = TypeVar("ProposedMessageType", BatchAppendReq.ProposedMessage, AppendReq.ProposedMessage)


@dataclass
class Message:
    event_type: str
    data: bytes | dict
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    custom_metadata: Optional[dict] = None

    def to_protobuf(self, message_type: Type[ProposedMessageType]) -> ProposedMessageType:
        assert isinstance(self.data, (bytes, dict))
        return message_type(
            id=UUID(string=str(self.id)),
            metadata={
                "type": self.event_type,
                "content-type": ContentType.OCTET_STREAM.value
                if isinstance(self.data, bytes)
                else ContentType.JSON.value,
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


@dataclass
class Filter:
    class Kind(enum.Enum):
        STREAM = "stream"
        EVENT_TYPE = "event_type"

    kind: Kind
    regex: str
    prefixes: Optional[list[str]] = None

    def to_protobuf(self) -> ReadReq.Options.FilterOptions:
        Expression = ReadReq.Options.FilterOptions.Expression
        stream_identifier = None
        event_type = None
        if self.kind == self.Kind.STREAM:
            stream_identifier = Expression(regex=self.regex, prefix=self.prefixes)
        elif self.kind == self.Kind.EVENT_TYPE:
            event_type = Expression(regex=self.regex, prefix=self.prefixes)
        return ReadReq.Options.FilterOptions(
            stream_identifier=stream_identifier,
            event_type=event_type,
            max=0,  # This apparently does nothing ¯\_(ツ)_/¯
            count=Empty(),
        )


class StreamsBase(abc.ABC):

    _stub: StreamsStub

    @staticmethod
    def _append_requests(
        stream: str,
        event_type: str,
        data: dict | bytes,
        stream_state: StreamState = StreamState.ANY,
        revision: None | int = None,
        custom_metadata: None | dict = None,
    ) -> Iterable[AppendReq]:
        if revision is not None:
            # Append at specified revision
            options = {"revision": revision}
        else:
            options: dict[str, None | Empty] = {v.value: None for v in StreamState}
            options[stream_state.value] = Empty()

        yield AppendReq(
            options=AppendReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **options,
            )
        )

        yield AppendReq(
            proposed_message=Message(
                event_type=event_type,
                data=data,
                custom_metadata=custom_metadata,
            ).to_protobuf(AppendReq.ProposedMessage)
        )

    @staticmethod
    def _process_append_response(response: AppendResp) -> AppendResult:
        if response.HasField("wrong_expected_version"):
            raise Exception(f"TODO: wrong expected version: {response.wrong_expected_version}")
        if not response.HasField("success"):
            raise Exception(f"TODO: {response}")
        return AppendResult.from_response(response)

    @abc.abstractmethod
    def append(
        self,
        stream: str,
        event_type: str,
        data: dict | bytes,
        stream_state: StreamState = StreamState.ANY,
        revision: None | int = None,
        custom_metadata: None | dict = None,
    ) -> Iterable[AppendReq]:
        ...

    @staticmethod
    def _read_request(
        stream: str,
        count: Optional[int],
        backwards: bool,
        revision: Optional[int],
        subscribe: bool,
    ) -> ReadReq:
        options = {}
        if revision is not None:
            options["revision"] = revision
        else:
            options.update(
                {
                    "start": None if backwards else Empty(),
                    "end": Empty() if backwards else None,
                }
            )
        return ReadReq(
            options=ReadReq.Options(
                stream=ReadReq.Options.StreamOptions(
                    stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                    **options,
                ),
                all=None,
                read_direction=ReadReq.Options.Backwards if backwards else ReadReq.Options.Forwards,
                resolve_links=True,  # Resolve to actual data instead of a link when reading from projection
                count=count,
                subscription=ReadReq.Options.SubscriptionOptions() if subscribe else None,
                filter=None,
                no_filter=Empty(),
                uuid_option=ReadReq.Options.UUIDOption(structured=Empty(), string=Empty()),
            )
        )

    @staticmethod
    def _read_all_request(count: Optional[int], backwards: bool, filter_by: Optional[Filter]) -> ReadReq:
        return ReadReq(
            options=ReadReq.Options(
                stream=None,
                all=ReadReq.Options.AllOptions(
                    start=None if backwards else Empty(),
                    end=Empty() if backwards else None,
                ),
                read_direction=ReadReq.Options.Backwards if backwards else ReadReq.Options.Forwards,
                # I can get subscription to work with filters, for some reason eventstore complains with
                # all possible combinations, so for now `read-all` only works with count
                subscription=None,
                resolve_links=True,
                count=count,
                filter=filter_by.to_protobuf() if filter_by else None,
                no_filter=None if filter_by else Empty(),
                uuid_option=ReadReq.Options.UUIDOption(structured=Empty(), string=Empty()),
            )
        )

    @staticmethod
    def _process_read_response(response: ReadResp) -> ReadResult:
        if response.HasField("stream_not_found"):
            raise Exception("TODO: Stream not found")
        return ReadResult.from_response(response)

    @abc.abstractmethod
    def read(
        self,
        stream: str,
        count: int,
        backwards: bool = False,
        revision: int | None = None,
    ) -> ReadResult:
        ...

    @staticmethod
    def _delete_request(
        stream: str, stream_state: StreamState = StreamState.ANY, revision: int | None = None
    ) -> DeleteReq:
        if revision is not None:
            options = {"revision": revision}
        else:
            options: dict[str, None | Empty] = {v.value: None for v in StreamState}
            options[stream_state.value] = Empty()

        return DeleteReq(
            options=DeleteReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **options,
            )
        )

    @staticmethod
    def _process_delete_response(response: DeleteResp) -> DeleteResult:
        return DeleteResult.from_response(response)

    @abc.abstractmethod
    def delete(
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: int | None = None
    ) -> DeleteResult:
        ...

    @staticmethod
    def _tombstone_request(
        stream: str, stream_state: StreamState = StreamState.ANY, revision: int | None = None
    ) -> TombstoneReq:
        if revision is not None:
            options = {"revision": revision}
        else:
            options: dict[str, None | Empty] = {v.value: None for v in StreamState}
            options[stream_state.value] = Empty()

        return TombstoneReq(
            options=TombstoneReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **options,
            )
        )

    @staticmethod
    def _process_tombstone_response(response: TombstoneResp) -> TombstoneResult:
        return TombstoneResult.from_response(response)

    @abc.abstractmethod
    def tombstone(
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: int | None = None
    ) -> TombstoneResult:
        ...

    @staticmethod
    def _batch_append_requests(
        stream: str,
        messages: Iterable[Message],
        stream_state: StreamState = StreamState.ANY,
        revision: int | None = None,
        correlation_id: None | uuid.UUID = None,
        deadline_ms: None | int = None,
    ) -> Iterable[BatchAppendReq]:
        correlation_id_ = UUID(string=str(correlation_id or uuid.uuid4()))
        options: dict[str, int | GEmpty | None]
        if revision is not None:
            # Append at specified revision
            options = {"revision": revision}
        else:
            options = {v.value: None for v in StreamState}
            options[stream_state.value] = GEmpty()

        if deadline_ms is not None:
            options["deadline"] = Duration(nanos=deadline_ms * 1000000)

        yield BatchAppendReq(
            correlation_id=correlation_id_,
            options=BatchAppendReq.Options(
                # stream_position=0,  # TODO: wtf is this? probably expected position
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **options,
            ),
            is_final=False,  # This needs to be off for options
        )
        yield BatchAppendReq(
            correlation_id=correlation_id_,
            proposed_messages=(m.to_protobuf(BatchAppendReq.ProposedMessage) for m in messages),
            is_final=True,
        )

    @staticmethod
    def _process_batch_append_response(response: BatchAppendResp) -> BatchAppendResult:
        if response.HasField("error"):
            raise Exception(f"TODO: got error {response.error}")
        if not response.HasField("success"):
            raise Exception(f"TODO: {response}")
        return BatchAppendResult.from_response(response)

    @abc.abstractmethod
    def batch_append(
        self,
        stream: str,
        messages: Iterable[Message],
        stream_state: StreamState = StreamState.ANY,
        revision: int | None = None,
        correlation_id: None | uuid.UUID = None,
        deadline_ms: None | int = None,
    ) -> BatchAppendResult:
        ...
