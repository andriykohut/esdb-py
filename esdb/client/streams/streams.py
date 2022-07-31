import logging
import uuid
from typing import AsyncIterable, Iterable, Optional, Union

import grpc
from google.protobuf.duration_pb2 import Duration
from google.protobuf.empty_pb2 import Empty as GEmpty

from esdb.client.exceptions import ClientException, StreamNotFound, WrongExpectedVersion
from esdb.client.streams.types import (
    AppendResult,
    BatchAppendResult,
    Checkpoint,
    DeleteResult,
    Filter,
    Message,
    ReadEvent,
    StreamState,
    SubscriptionConfirmed,
    TombstoneResult,
)
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

logger = logging.getLogger(__name__)


class Streams:
    def __init__(self, stub: StreamsStub) -> None:
        self._stub = stub

    @staticmethod
    def _append_requests(
        stream: str,
        event_type: str,
        data: Union[dict, bytes],
        stream_state: StreamState = StreamState.ANY,
        revision: Optional[int] = None,
        custom_metadata: Optional[dict] = None,
    ) -> Iterable[AppendReq]:
        options = AppendReq.Options(
            stream_identifier=StreamIdentifier(stream_name=stream.encode()),
            **{stream_state.value: Empty()},  # type: ignore
        )
        if revision is not None:
            # Append at specified revision
            options.revision = revision
        yield AppendReq(options=options)

        yield AppendReq(
            proposed_message=Message(
                event_type=event_type,
                data=data,
                custom_metadata=custom_metadata,
            ).to_protobuf(AppendReq.ProposedMessage)
        )

    @staticmethod
    def _process_append_response(response: AppendResp) -> AppendResult:
        if response.WhichOneof("result") == "wrong_expected_version":
            raise WrongExpectedVersion(response.wrong_expected_version)
        return AppendResult.from_response(response)

    async def append(  # type: ignore
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

    @staticmethod
    def _read_request(
        stream: str,
        count: Optional[int],
        revision: Optional[int],
        backwards: bool,
        subscribe: bool,
    ) -> ReadReq:
        stream_options = ReadReq.Options.StreamOptions(
            stream_identifier=StreamIdentifier(stream_name=stream.encode()),
            start=None if backwards else Empty(),
            end=Empty() if backwards else None,
        )
        if revision is not None:
            stream_options.revision = revision
        options = ReadReq.Options(
            stream=stream_options,
            all=None,
            read_direction=ReadReq.Options.Backwards if backwards else ReadReq.Options.Forwards,
            resolve_links=True,  # Resolve to actual data instead of a link when reading from projection
            subscription=ReadReq.Options.SubscriptionOptions() if subscribe else None,
            filter=None,
            no_filter=Empty(),
            uuid_option=ReadReq.Options.UUIDOption(structured=Empty(), string=Empty()),
        )
        if count:
            options.count = count
        return ReadReq(options=options)

    @staticmethod
    def _read_all_request(
        count: Optional[int],
        subscribe: bool,
        backwards: bool,
        filter_by: Optional[Filter],
    ) -> ReadReq:
        assert subscribe ^ (count is not None), "subscribe and count are mutually exclusive arguments"
        req = ReadReq(
            options=ReadReq.Options(
                stream=None,
                all=ReadReq.Options.AllOptions(
                    start=None if backwards else Empty(),
                    end=Empty() if backwards else None,
                    # position=ReadReq.Options.Position()  # TODO: implement position
                ),
                read_direction=ReadReq.Options.Backwards if backwards else ReadReq.Options.Forwards,
                resolve_links=True,
                subscription=ReadReq.Options.SubscriptionOptions() if subscribe else None,
                filter=filter_by.to_protobuf() if filter_by else None,
                no_filter=None if filter_by else Empty(),
                uuid_option=ReadReq.Options.UUIDOption(structured=Empty(), string=Empty()),
            )
        )
        if count is not None:
            req.options.count = count
        if subscribe and filter_by:
            assert (
                filter_by.checkpoint_interval_multiplier is not None
            ), "checkpoint_interval_multiplier is required when subscribing"
        return req

    @staticmethod
    def _process_read_response(response: ReadResp) -> Union[ReadEvent, SubscriptionConfirmed, Checkpoint]:
        content = response.WhichOneof("content")
        if content == "event":
            return ReadEvent.from_response(response)
        if content == "confirmation":
            return SubscriptionConfirmed(response.confirmation.subscription_id)
        if content == "checkpoint":
            return Checkpoint(
                commit_position=response.checkpoint.commit_position,
                prepare_position=response.checkpoint.prepare_position,
            )
        if content == "stream_not_found":
            raise StreamNotFound(response.stream_not_found)
        raise ClientException(f"Got unexpected response {content}: {getattr(response, content)}")  # type: ignore

    async def read(  # type: ignore
        self,
        stream: str,
        count: Optional[int] = None,
        backwards: bool = False,
        revision: Optional[int] = None,
        subscribe: bool = False,
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
        self, count: Optional[int] = None, backwards=False, subscribe=False, filter_by: Optional[Filter] = None
    ) -> AsyncIterable[ReadEvent]:
        request = self._read_all_request(
            count=count,
            subscribe=subscribe,
            backwards=backwards,
            filter_by=filter_by,
        )
        async for response in self._read_iter(self._stub.Read(request)):
            yield response

    @staticmethod
    def _delete_request(
        stream: str, stream_state: StreamState = StreamState.ANY, revision: Optional[int] = None
    ) -> DeleteReq:
        req = DeleteReq(
            options=DeleteReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **{stream_state.value: Empty()},  # type: ignore
            )
        )
        if revision is not None:
            req.options.revision = revision
        return req

    @staticmethod
    def _process_delete_response(response: DeleteResp) -> Optional[DeleteResult]:
        has_position = response.WhichOneof("position_option") == "position"
        return DeleteResult.from_response(response) if has_position else None

    async def delete(  # type: ignore
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: Optional[int] = None
    ) -> Optional[DeleteResult]:
        request = self._delete_request(stream=stream, stream_state=stream_state, revision=revision)
        try:
            response = await self._stub.Delete(request)
        except grpc.aio._call.AioRpcError as err:  # type: ignore
            raise ClientException(f"Delete failed: {err.details()}") from err
        return self._process_delete_response(response)

    @staticmethod
    def _tombstone_request(
        stream: str, stream_state: StreamState = StreamState.ANY, revision: Optional[int] = None
    ) -> TombstoneReq:
        req = TombstoneReq(
            options=TombstoneReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **{stream_state.value: Empty()},  # type: ignore
            )
        )
        if revision is not None:
            req.options.revision = revision
        return req

    @staticmethod
    def _process_tombstone_response(response: TombstoneResp) -> Optional[TombstoneResult]:
        has_position = response.WhichOneof("position_option") == "position"
        return TombstoneResult.from_response(response) if has_position else None

    async def tombstone(  # type: ignore
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: Optional[int] = None
    ) -> Optional[TombstoneResult]:
        request = self._tombstone_request(stream=stream, stream_state=stream_state, revision=revision)
        response = await self._stub.Tombstone(request)
        return self._process_tombstone_response(response)

    @staticmethod
    def _batch_append_requests(
        stream: str,
        messages: Iterable[Message],
        stream_state: StreamState = StreamState.ANY,
        correlation_id: Optional[uuid.UUID] = None,
        deadline_ms: Optional[int] = None,
        stream_position: Optional[int] = None,
    ) -> Iterable[BatchAppendReq]:
        correlation_id_ = UUID(string=str(correlation_id or uuid.uuid4()))
        options_req = BatchAppendReq(
            correlation_id=correlation_id_,
            options=BatchAppendReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                deadline=Duration(nanos=deadline_ms * 1000000) if deadline_ms is not None else None,
                **{stream_state.value: GEmpty()},  # type: ignore
            ),
            is_final=False,
        )
        if stream_position is not None:
            options_req.options.stream_position = stream_position
        yield options_req
        yield BatchAppendReq(
            correlation_id=correlation_id_,
            proposed_messages=(m.to_protobuf(BatchAppendReq.ProposedMessage) for m in messages),
            is_final=True,
        )

    @staticmethod
    def _process_batch_append_response(response: BatchAppendResp) -> BatchAppendResult:
        result = response.WhichOneof("result")
        if result == "error":
            # For some reason ES uses google.rpc.Status here instead of more meaningful error.
            raise ClientException(f"Append failed with {response.error.message} and code {response.error.code}")
        return BatchAppendResult.from_response(response)

    async def batch_append(  # type: ignore
        self,
        stream: str,
        messages: Iterable[Message],
        stream_state: StreamState = StreamState.ANY,
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
            result = self._process_batch_append_response(response)
            return result
