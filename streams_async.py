from shared_pb2 import Empty, StreamIdentifier
from streams import StreamState, AppendResult, Message
from streams_pb2 import AppendReq, AppendResp
from streams_pb2_grpc import StreamsStub


# TODO: This is just a stub to see if the things are working - refactor this to reuse what we already have for
#       non-async client since the only difference in `await self._stub.Method(...)` vs `self._stub.Method(...)`

class Streams:
    def __init__(self, streams_stub: StreamsStub) -> None:
        self._stub = streams_stub

    async def append(
        self,
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
            proposed_message=Message(
                event_type=event_type,
                data=data,
                custom_metadata=custom_metadata,
            ).to_protobuf(AppendReq.ProposedMessage)
        )

        append_response: AppendResp = await self._stub.Append(iter([options, proposed_message]))

        if append_response.HasField("wrong_expected_version"):
            raise Exception(f"TODO: wrong expected version: {append_response.wrong_expected_version}")
        if not append_response.HasField("success"):
            raise Exception(f"TODO: {append_response}")
        return AppendResult.from_response(append_response)
