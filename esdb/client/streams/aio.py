import logging
import uuid
from typing import AsyncIterable, Iterable, Optional, Union

import grpc

from esdb.client.exceptions import ClientException
from esdb.client.streams.base import (
    AppendResult,
    BatchAppendResult,
    Checkpoint,
    DeleteResult,
    Filter,
    Message,
    ReadEvent,
    StreamsBase,
    StreamState,
    SubscriptionConfirmed,
    TombstoneResult,
)
from esdb.generated.streams_pb2 import ReadResp
from esdb.generated.streams_pb2_grpc import StreamsStub

logger = logging.getLogger(__name__)


class Streams(StreamsBase):
    def __init__(self, stub: StreamsStub) -> None:
        self._stub = stub

    async def append(
        self,
        stream: str,
        event_type: str,
        data: Union[dict, bytes],
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

    async def _read_iter(self, responses: AsyncIterable[ReadResp]) -> AsyncIterable[ReadEvent]:
        async for response in responses:
            response = self._process_read_response(response)
            if isinstance(response, ReadEvent):
                yield response
            elif isinstance(response, SubscriptionConfirmed):
                logger.info(f"Subscription {response.subscription_id} confirmed")
            elif isinstance(response, Checkpoint):
                logger.info(
                    f"Checkpoint commit position: {response.commit_position}, "
                    f"prepare position: {response.prepare_position}"
                )

    async def read(
        self, stream: str, count: int, backwards: bool = False, revision: Optional[int] = None, subscribe: bool = False
    ) -> AsyncIterable[ReadEvent]:
        assert (count is not None) ^ subscribe, "count or subscribe is required"
        request = self._read_request(
            stream=stream,
            count=count,
            backwards=backwards,
            revision=revision,
            subscribe=subscribe,
        )
        async for response in self._read_iter(self._stub.Read(request)):
            yield response

    async def read_all(
        self, count: int, backwards=False, filter_by: Optional[Filter] = None
    ) -> AsyncIterable[ReadEvent]:
        request = self._read_all_request(
            count=count,
            backwards=backwards,
            filter_by=filter_by,
        )
        async for response in self._read_iter(self._stub.Read(request)):
            yield response

    async def delete(
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: Optional[int] = None
    ) -> Optional[DeleteResult]:
        request = self._delete_request(stream=stream, stream_state=stream_state, revision=revision)
        try:
            response = await self._stub.Delete(request)
        except grpc.aio._call.AioRpcError as err:
            raise ClientException(f"Delete failed: {err.details()}") from err
        return self._process_delete_response(response)

    async def tombstone(
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: Optional[int] = None
    ) -> Optional[TombstoneResult]:
        request = self._tombstone_request(stream=stream, stream_state=stream_state, revision=revision)
        response = await self._stub.Tombstone(request)
        return self._process_tombstone_response(response)

    async def batch_append(
        self,
        stream: str,
        messages: Iterable[Message],
        stream_state: StreamState = StreamState.ANY,
        revision: Optional[int] = None,
        correlation_id: Optional[uuid.UUID] = None,
        deadline_ms: Optional[int] = None,
    ) -> BatchAppendResult:
        requests = self._batch_append_requests(
            stream=stream,
            messages=messages,
            stream_state=stream_state,
            correlation_id=correlation_id,
            deadline_ms=deadline_ms,
        )
        async for response in self._stub.BatchAppend(requests):
            return self._process_batch_append_response(response)
