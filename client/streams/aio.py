import uuid
from typing import Iterable, Optional

from client.streams.base import (
    AppendResult,
    BatchAppendResult,
    DeleteResult,
    Message,
    ReadResult,
    StreamsBase,
    StreamState,
    TombstoneResult,
)
from streams_pb2_grpc import StreamsStub


class Streams(StreamsBase):
    def __init__(self, stub: StreamsStub) -> None:
        self._stub = stub

    async def append(
        self,
        stream: str,
        event_type: str,
        data: dict | bytes,
        stream_state: StreamState = StreamState.ANY,
        revision: Optional[int] = None,
        custom_metadata: Optional[dict] = None,
    ) -> AppendResult:
        requests = self._append_requests(
            stream=stream,
            event_type=event_type,
            data=data,
            stream_state=stream_state,
            revision=revision,
            custom_metadata=custom_metadata,
        )
        response = await self._stub.Append(requests)
        return self._process_append_response(response)

    async def read(
        self,
        stream: str,
        count: int,
        backwards: bool = False,
        revision: Optional[int] = None,
    ) -> Iterable[ReadResult]:
        request = self._read_request(
            stream=stream,
            count=count,
            backwards=backwards,
            revision=revision,
        )
        response = await self._stub.Read(request)
        return self._process_read_responses(response)

    async def delete(
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: int | None = None
    ) -> DeleteResult:
        request = self._delete_request(stream=stream, stream_state=stream_state, revision=revision)
        response = await self._stub.Delete(request)
        return self._process_delete_response(response)

    async def tombstone(
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: int | None = None
    ) -> TombstoneResult:
        request = self._tombstone_request(stream=stream, stream_state=stream_state, revision=revision)
        response = await self._stub.Tombstone(request)
        return self._process_tombstone_response(response)

    async def batch_append(
        self,
        stream: str,
        messages: Iterable[Message],
        stream_state: StreamState = StreamState.ANY,
        revision: int | None = None,
        correlation_id: None | uuid.UUID = None,
        deadline_ms: None | int = None,
    ) -> BatchAppendResult:
        requests = self._batch_append_requests(
            stream=stream,
            messages=messages,
            stream_state=stream_state,
            revision=revision,
            correlation_id=correlation_id,
            deadline_ms=deadline_ms,
        )
        responses = await self._stub.BatchAppend(requests)
        return self._process_batch_append_responses(responses)
