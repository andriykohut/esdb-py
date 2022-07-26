from __future__ import annotations

import enum
import json
import uuid
from dataclasses import dataclass
from typing import Iterable

from google.protobuf.duration_pb2 import Duration
from google.protobuf.empty_pb2 import Empty as GEmpty

from shared_pb2 import UUID, Empty, StreamIdentifier
from streams_pb2 import (
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
from streams_pb2_grpc import StreamsStub


@enum.unique
class StreamState(enum.Enum):
    ANY = "any"
    NO_STREAM = "no_stream"
    STREAM_EXISTS = "stream_exists"


@enum.unique
class ReadFrom(enum.Enum):
    START = "start"
    END = "end"


@enum.unique
class ContentType(enum.Enum):
    OCTET_STREAM = "application/octet-stream"
    JSON = "application/json"


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


@dataclass
class ReadResult:
    id: str
    stream_name: str
    prepare_position: int
    commit_position: int
    metadata: dict
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
        )


class Streams:
    def __init__(self, streams_stub: StreamsStub) -> None:
        self._stub = streams_stub

    def append(
        self,
        *,
        stream: str,
        event_type: str,
        data: dict | bytes,
        stream_state: StreamState = StreamState.ANY,
        revision: None | int = None,
        custom_metadata: None | dict = None,
    ) -> AppendResult:
        if revision is not None:
            # Append at specified revision
            options = {"revision": revision}
        else:
            options: dict[str, None | Empty] = {v.value: None for v in StreamState}
            options[stream_state.value] = Empty()
        options = AppendReq(
            options=AppendReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **options,
            )
        )
        proposed_message = AppendReq(
            proposed_message=AppendReq.ProposedMessage(
                id=UUID(string=str(uuid.uuid4())),
                metadata={
                    "type": event_type,
                    "content-type": ContentType.OCTET_STREAM.value
                    if isinstance(data, bytes)
                    else ContentType.JSON.value,
                },
                custom_metadata=json.dumps(custom_metadata).encode() if custom_metadata else b"",
                data=json.dumps(data).encode() if isinstance(data, dict) else data,
            ),
        )

        append_response: AppendResp = self._stub.Append(iter([options, proposed_message]))

        if append_response.HasField("wrong_expected_version"):
            raise Exception(f"TODO: wrong expected version: {append_response.wrong_expected_version}")
        if not append_response.HasField("success"):
            raise Exception(f"TODO: {append_response}")
        return AppendResult.from_response(append_response)

    def read(
        self,
        *,
        stream: str,
        count: int,
        backwards: bool = False,
        revision: int | None = None,
    ) -> Iterable[ReadResult]:
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
        read_request = ReadReq(
            options=ReadReq.Options(
                stream=ReadReq.Options.StreamOptions(
                    stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                    **options,
                ),
                all=None,
                read_direction=ReadReq.Options.Backwards if backwards else ReadReq.Options.Forwards,
                resolve_links=True,  # Resolve to actual data instead of a link when reading from projection
                count=count,
                subscription=None,  # TODO: Deal with subscriptions
                filter=None,  # TODO: Deal with filters
                no_filter=Empty(),
                uuid_option=ReadReq.Options.UUIDOption(structured=Empty(), string=Empty()),
            )
        )
        for response in self._stub.Read(read_request):
            response: ReadResp
            if response.HasField("stream_not_found"):
                raise Exception("TODO: Stream not found")
            yield ReadResult.from_response(response)

    def delete(
        self, *, stream: str, stream_state: StreamState = StreamState.ANY, revision: int | None = None
    ) -> DeleteResult:
        if revision is not None:
            options = {"revision": revision}
        else:
            options: dict[str, None | Empty] = {v.value: None for v in StreamState}
            options[stream_state.value] = Empty()

        delete_request = DeleteReq(
            options=DeleteReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **options,
            )
        )

        response = self._stub.Delete(delete_request)
        return DeleteResult.from_response(response)

    def tombstone(
        self, *, stream: str, stream_state: StreamState = StreamState.ANY, revision: int | None = None
    ) -> TombstoneResult:
        if revision is not None:
            options = {"revision": revision}
        else:
            options: dict[str, None | Empty] = {v.value: None for v in StreamState}
            options[stream_state.value] = Empty()

        tombstone_request = TombstoneReq(
            options=TombstoneReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **options,
            )
        )
        response = self._stub.Tombstone(tombstone_request)
        return TombstoneResult.from_response(response)

    def batch_append(
        self,
        *,
        stream: str,
        event_type: str,
        data: Iterable[dict | bytes],
        stream_state: StreamState = StreamState.ANY,
        revision: int | None = None,
        custom_metadata: None | dict = None,
        correlation_id: None | uuid.UUID = None,
        deadline_seconds: None | int = None,
        deadline_nanos: None | int = None,
    ) -> "BatchAppendResult":
        correlation_id = UUID(string=str(correlation_id or uuid.uuid4()))
        if revision is not None:
            # Append at specified revision
            options = {"revision": revision}
        else:
            options: dict[str, None | GEmpty] = {v.value: None for v in StreamState}
            options[stream_state.value] = GEmpty()
        options = BatchAppendReq(
            correlation_id=correlation_id,
            options=BatchAppendReq.Options(
                stream_position=0,  # TODO: wtf is position?
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                # #TODO: deadline=Duration(seconds=deadline_seconds, nanos=deadline_nanos),
                **options,
            ),
            is_final=False,  # This needs to be off for options
        )
        proposed_messages = BatchAppendReq(
            correlation_id=correlation_id,
            proposed_messages=(
                BatchAppendReq.ProposedMessage(
                    id=UUID(string=str(uuid.uuid4())),
                    metadata={
                        "type": event_type,
                        "content-type": ContentType.OCTET_STREAM.value
                        if isinstance(data, bytes)
                        else ContentType.JSON.value,
                    },
                    custom_metadata=json.dumps(custom_metadata).encode() if custom_metadata else b"",
                    data=json.dumps(item).encode() if isinstance(item, dict) else item,
                )
                for item in data
            ),
            is_final=True,  # TODO - figure out what to do with this
        )

        append_response_iter = self._stub.BatchAppend(iter([options, proposed_messages]))
        # __import__("ipdb").set_trace()
        for appemd_resp in append_response_iter:
            append_response: BatchAppendResp
            # if append_response.HasField("wrong_expected_version"):
            #     raise Exception(f"TODO: wrong expected version: {append_response.wrong_expected_version}")
            # if not append_response.HasField("success"):
            #     raise Exception(f"TODO: {append_response}")
            # return BatchAppendResult.from_response(append_response)
