import logging
import uuid
from typing import AsyncIterable, Iterable, Optional, Union

import grpc
from google.protobuf.duration_pb2 import Duration
from google.protobuf.empty_pb2 import Empty as GEmpty

from esdb.exceptions import ClientException, StreamNotFound, WrongExpectedVersion
from esdb.generated.shared_pb2 import UUID, Empty, StreamIdentifier
from esdb.generated.streams_pb2 import (
    AppendReq,
    AppendResp,
    BatchAppendReq,
    DeleteReq,
    DeleteResp,
    ReadReq,
    ReadResp,
    TombstoneReq,
    TombstoneResp,
)
from esdb.generated.streams_pb2_grpc import StreamsStub
from esdb.shared import Filter
from esdb.streams.types import (
    AppendResult,
    BatchAppendResult,
    Checkpoint,
    DeleteResult,
    Message,
    ReadEvent,
    StreamState,
    SubscriptionConfirmed,
    TombstoneResult,
)

logger = logging.getLogger(__name__)


class Streams:
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

        options = AppendReq.Options(
            stream_identifier=StreamIdentifier(stream_name=stream.encode()),
            **{stream_state.value: Empty()},  # type: ignore
        )
        if revision is not None:
            # Append at specified revision
            options.revision = revision
        requests = [
            AppendReq(options=options),
            AppendReq(
                proposed_message=Message(
                    event_type=event_type,
                    data=data,
                    custom_metadata=custom_metadata,
                ).to_protobuf(AppendReq.ProposedMessage)
            ),
        ]
        response: AppendResp = await self._stub.Append(requests)
        if response.WhichOneof("result") == "wrong_expected_version":
            raise WrongExpectedVersion(response.wrong_expected_version)
        return AppendResult.from_response(response)

    async def _get_events(self, responses: AsyncIterable[ReadResp]) -> AsyncIterable[ReadEvent]:
        """Filter out the responses from read requests, since we only care about read events."""
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

    async def read(
        self,
        stream: str,
        count: Optional[int] = None,
        backwards: bool = False,
        revision: Optional[int] = None,
        subscribe: bool = False,
    ) -> AsyncIterable[ReadEvent]:
        assert (count is not None) ^ subscribe, "count or subscribe is required"

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
        if count is not None:
            options.count = count

        async for response in self._get_events(self._stub.Read(ReadReq(options=options))):
            yield response

    async def read_all(
        self, count: Optional[int] = None, backwards=False, subscribe=False, filter_by: Optional[Filter] = None
    ) -> AsyncIterable[ReadEvent]:

        assert subscribe ^ (count is not None), "subscribe and count are mutually exclusive arguments"
        request = ReadReq(
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
                filter=filter_by.to_protobuf(ReadReq.Options.FilterOptions) if filter_by else None,
                no_filter=None if filter_by else Empty(),
                uuid_option=ReadReq.Options.UUIDOption(structured=Empty(), string=Empty()),
            )
        )
        if count is not None:
            request.options.count = count
        if subscribe and filter_by:
            assert (
                filter_by.checkpoint_interval_multiplier is not None
            ), "checkpoint_interval_multiplier is required when subscribing"
        async for response in self._get_events(self._stub.Read(request)):
            yield response

    async def delete(
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: Optional[int] = None
    ) -> Optional[DeleteResult]:
        request = DeleteReq(
            options=DeleteReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **{stream_state.value: Empty()},  # type: ignore
            )
        )
        if revision is not None:
            request.options.revision = revision
        try:
            response: DeleteResp = await self._stub.Delete(request)
        except grpc.aio._call.AioRpcError as err:  # type: ignore
            raise ClientException(f"Delete failed: {err.details()}") from err
        has_position = response.WhichOneof("position_option") == "position"
        return DeleteResult.from_response(response) if has_position else None

    async def tombstone(
        self, stream: str, stream_state: StreamState = StreamState.ANY, revision: Optional[int] = None
    ) -> Optional[TombstoneResult]:
        request = TombstoneReq(
            options=TombstoneReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                **{stream_state.value: Empty()},  # type: ignore
            )
        )
        if revision is not None:
            request.options.revision = revision
        response: TombstoneResp = await self._stub.Tombstone(request)
        has_position = response.WhichOneof("position_option") == "position"
        return TombstoneResult.from_response(response) if has_position else None

    async def batch_append(
        self,
        stream: str,
        messages: Iterable[Message],
        stream_state: Optional[StreamState] = None,
        correlation_id: Optional[uuid.UUID] = None,
        deadline_ms: Optional[int] = None,
        stream_position: Optional[int] = None,
    ) -> BatchAppendResult:
        if stream_position is not None and stream_state is not None:
            raise ValueError("stream_position can't be used with stream_state")
        if stream_position is None and stream_state is None:
            stream_state = StreamState.ANY
        correlation_id_ = UUID(string=str(correlation_id or uuid.uuid4()))
        stream_opts = {stream_state.value: GEmpty()} if stream_state else {}
        options_req = BatchAppendReq(
            correlation_id=correlation_id_,
            options=BatchAppendReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                deadline=Duration(nanos=deadline_ms * 1000000) if deadline_ms is not None else None,
                **stream_opts,  # type: ignore
            ),
            is_final=False,
        )
        if stream_position is not None:
            options_req.options.stream_position = stream_position

        requests = [
            options_req,
            BatchAppendReq(
                correlation_id=correlation_id_,
                proposed_messages=(m.to_protobuf(BatchAppendReq.ProposedMessage) for m in messages),
                is_final=True,
            ),
        ]
        result = None
        async for response in self._stub.BatchAppend(requests):
            if response.WhichOneof("result") == "error":
                # For some reason ES uses google.rpc.Status here instead of more meaningful error.
                raise ClientException(f"Append failed with {response.error.message} and code {response.error.code}")
            result = BatchAppendResult.from_response(response)
            # TODO: Handle streaming of multiple batches and responses
            break
        assert result
        return result
