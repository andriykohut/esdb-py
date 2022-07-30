from esdb.generated.shared_pb2 import Empty
from esdb.generated.streams_pb2 import AppendResp, ReadResp


class ClientException(Exception):
    ...


class WrongExpectedVersion(ClientException):
    def __init__(self, error: AppendResp.wrong_expected_version):
        expected_revision = error.WhichOneof("expected_revision_option")
        expected_val = getattr(error, expected_revision)
        current_revision = error.WhichOneof("current_revision_option")
        current_val = getattr(error, current_revision)

        expected = (
            expected_revision if isinstance(expected_val, Empty) else f"{expected_revision}={expected_val}"
        ).replace("expected_", "")

        current = (
            current_revision if isinstance(current_val, Empty) else f"{current_revision}={current_val}"
        ).replace("current_", "")

        super().__init__(f"Expected state '{expected}', got '{current}'")


class StreamNotFound(ClientException):
    def __init__(self, error: ReadResp.StreamNotFound) -> None:
        super().__init__(f"Stream '{error.stream_identifier.stream_name.decode()}' not found")
