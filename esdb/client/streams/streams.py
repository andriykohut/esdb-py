import logging
import uuid
from typing import Iterable, Optional, Union

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

    def append(
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
        response = self._stub.Append(requests)
        return self._process_append_response(response)

    def _read_iter(self, responses: Iterable[ReadResp]) -> Iterable[ReadEvent]:
        for response in responses:
            result = self._process_read_response(response)
            if isinstance(result, ReadEvent):
                yield result
            elif isinstance(result, SubscriptionConfirmed):
                logger.info(f"Subscription {result.subscription_id} confirmed")
            elif isinstance(result, Checkpoint):
                logger.info(
                    f"Checkpoint commit position: {result.commit_position}, "
                    f"prepare position: {result.prepare_position}"
                )

    def read(
        self,
        stream: str,
        count: Optional[int] = None,
        backwards: bool = False,
        revision: Optional[int] = None,
        subscribe: bool = False,
    ) -> Iterable[ReadEvent]:
        assert (count is not None) ^ subscribe, "count or subscribe is required"
        request = self._read_request(
            stream=stream,
            count=count,
            backwards=backwards,
            revision=revision,
            subscribe=subscribe,
        )

        yield from self._read_iter(self._stub.Read(request))

    def read_all(
        self, count: Optional[int] = None, subscribe=False, backwards=False, filter_by: Optional[Filter] = None
    ) -> Iterable[ReadEvent]:
        request = self._read_all_request(
            count=count,
            subscribe=subscribe,
            backwards=backwards,
            filter_by=filter_by,
        )
        yield from self._read_iter(self._stub.Read(request))

    def delete(
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: Optional[int] = None
    ) -> Optional[DeleteResult]:
        request = self._delete_request(stream=stream, stream_state=stream_state, revision=revision)
        try:
            response = self._stub.Delete(request)
        except grpc._channel._InactiveRpcError as err:  # type: ignore
            raise ClientException(f"Delete failed: {err.details()}") from err
        return self._process_delete_response(response)

    def tombstone(
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: Optional[int] = None
    ) -> Optional[TombstoneResult]:
        request = self._tombstone_request(stream=stream, stream_state=stream_state, revision=revision)
        response = self._stub.Tombstone(request)
        return self._process_tombstone_response(response)

    def batch_append(
        self,
        stream: str,
        messages: Iterable[Message],
        stream_state: StreamState = StreamState.ANY,
        correlation_id: Optional[uuid.UUID] = None,
        deadline_ms: Optional[int] = None,
        stream_position: Optional[int] = None,
    ) -> BatchAppendResult:
        requests = self._batch_append_requests(
            stream=stream,
            messages=messages,
            stream_state=stream_state,
            correlation_id=correlation_id,
            deadline_ms=deadline_ms,
            stream_position=stream_position,
        )
        # TODO: Implement streaming append iterator, for now we always deal with one batch
        response = next(self._stub.BatchAppend(requests))
        return self._process_batch_append_response(response)
