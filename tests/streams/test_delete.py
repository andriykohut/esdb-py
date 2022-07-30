import uuid

import grpc
import pytest

from esdb.client.exceptions import StreamNotFound
from esdb.client.streams import StreamState
from esdb.client.streams.base import DeleteResult


def test_delete_stream(client):
    stream = str(uuid.uuid4())
    with client.connect() as conn:
        conn.streams.append(stream=stream, event_type="foobar", data=b"a")
        conn.streams.append(stream=stream, event_type="foobar", data=b"b")

        assert len(list(conn.streams.read(stream=stream, count=20))) == 2

        result = conn.streams.delete(stream=stream)

    assert isinstance(result, DeleteResult)
    assert isinstance(result.commit_position, int)
    assert isinstance(result.prepare_position, int)

    with client.connect() as conn:
        with pytest.raises(StreamNotFound) as err:
            next(conn.streams.read(stream=stream, count=20))

    assert str(err.value) == f"Stream '{stream}' not found"


def test_delete_stream_with_revision(client):
    stream = str(uuid.uuid4())
    with client.connect() as conn:
        for i in range(3):
            conn.streams.append(stream=stream, event_type="foobar", data=f"{i}".encode())

        assert len(list(conn.streams.read(stream=stream, count=20))) == 3

        # TODO: this should be a custom exception
        with pytest.raises(grpc._channel._InactiveRpcError) as err:
            conn.streams.delete(stream=stream, revision=1)

        assert "Expected version: 1, Actual version: 2" in str(err.value)
        conn.streams.delete(stream=stream, revision=2)


def test_delete_with_stream_state(client):
    stream1 = str(uuid.uuid4())
    stream2 = str(uuid.uuid4())
    stream3 = str(uuid.uuid4())
    with client.connect() as conn:
        conn.streams.append(stream=stream1, event_type="foobar", data=b"")
        conn.streams.append(stream=stream2, event_type="foobar", data=b"")
        conn.streams.delete(stream=stream1, stream_state=StreamState.STREAM_EXISTS)
        # TODO: this should be a custom exception
        with pytest.raises(grpc._channel._InactiveRpcError) as err:
            conn.streams.delete(stream=stream2, stream_state=StreamState.NO_STREAM)

        assert "Expected version: -1, Actual version: 0" in str(err)

        with pytest.raises(grpc._channel._InactiveRpcError):
            # This doesn't make sense, since why would someone would delete stream if they think it doesn't exist?
            conn.streams.delete(stream=stream3, stream_state=StreamState.NO_STREAM)

        with pytest.raises(grpc._channel._InactiveRpcError) as err:
            conn.streams.delete(stream=stream3)

        assert "Expected version: -2, Actual version: -1" in str(err)
