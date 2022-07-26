import enum
import json
import uuid
from dataclasses import dataclass

import grpc
from streams_pb2 import AppendReq, AppendResp, ReadReq, ReadResp
from streams_pb2_grpc import StreamsStub
from shared_pb2 import Empty, StreamIdentifier, UUID


class StreamState(enum.Enum):
    ANY = "any"
    NO_STREAM = "no_stream"
    STREAM_EXISTS = "stream_exists"


class ReadFrom(enum.Enum):
    START = "start"
    END = "end"

class ContentType(enum.Enum):
    OCTET_STREAM = 'application/octet-stream'
    JSON = 'application/json'


@dataclass
class AppendResult:
    current_revision: int
    commit_position: int
    prepare_position: int

@dataclass
class ReadResult:
    id: str
    stream_name: str
    prepare_position: int
    commit_position: int
    metadata: dict
    custom_metadata: bytes
    data: dict | bytes

    @staticmethod
    def from_read_response(response: ReadResp) -> 'ReadResult':
        return ReadResult(
            id=response.event.event.id.string,
            stream_name=response.event.event.stream_identifier.stream_name.decode(),
            metadata=response.event.event.metadata,
            custom_metadata=response.event.event.custom_metadata,
            data=json.loads(response.event.event.data) if response.event.event.metadata['content-type'] == ContentType.JSON.value else response.event.event.data,
            prepare_position=response.event.commit_position,
            commit_position=response.event.commit_position,
        )


class Streams:
    def __init__(self, streams_stub: StreamsStub) -> None:
        self._stub = streams_stub

    def append(
        self,
        stream: str,
        event_type: str,
        data: dict | bytes,
        stream_state: StreamState = StreamState.ANY,
    ):
        stream_state_args: dict[str, None | Empty] = {v.value: None for v in StreamState}
        stream_state_args[stream_state.value] = Empty()
        options = AppendReq(
            options=AppendReq.Options(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                revision=1,  # TODO: Figure out what this does?
                **stream_state_args,
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
                custom_metadata=b"{}",
                data=json.dumps(data).encode() if isinstance(data, dict) else data,
            ),
        )

        append_response: AppendResp = self._stub.Append(iter([options, proposed_message]))

        if append_response.HasField("wrong_expected_version"):
            raise Exception(
                f"TODO: wrong expected version: {append_response.wrong_expected_version}"
            )
        if not append_response.HasField("success"):
            raise Exception(f"TODO: {append_response}")
        return AppendResult(
            current_revision=append_response.success.current_revision,
            commit_position=append_response.success.position.commit_position,
            prepare_position=append_response.success.position.prepare_position,
        )

    def read(self, stream: str, count: int, read_from: ReadFrom = ReadFrom.START) -> 'TODO':
        stream_options = {v.value: None for v in ReadFrom}
        stream_options[read_from.value] = Empty()
        read_request = ReadReq(options=ReadReq.Options(
            stream=ReadReq.Options.StreamOptions(
                stream_identifier=StreamIdentifier(stream_name=stream.encode()),
                revision=1,  # TODO figure out what this does?
                **stream_options,
            ),
            all=None,  # TODO: Does this mean read all?
            read_direction=ReadReq.Options.Forwards,  # TODO: How is this different to star/end in stream identifier?
            resolve_links=False,  # TODO: figure out what this does
            count=count,  # TODO: How many messages to read?
            subscription=None,  # TODO: Deal with subscriptions
            filter=None,  # TODO: Deal with filters
            no_filter=Empty(),
            uuid_option=ReadReq.Options.UUIDOption(structured=Empty(), string=Empty())
        ))
        for response in self._stub.Read(read_request):
            response: ReadResp
            yield ReadResult.from_read_response(response)



channel = grpc.insecure_channel("localhost:2113")
stub = StreamsStub(channel)
streams = Streams(stub)
result = streams.append(
    "test",
    event_type="order_placed",
    data={"x": 1, "y": 2},
)
for result in streams.read("test", 10):
    print(result)
