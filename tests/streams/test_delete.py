import uuid

import grpc
import pytest

from streams import DeleteResult


def test_delete_stream(client):
    stream = str(uuid.uuid4())
    client.streams.append(stream=stream, event_type="foobar", data=b"a")
    client.streams.append(stream=stream, event_type="foobar", data=b"b")

    assert len(list(client.streams.read(stream=stream, count=20))) == 2

    result = client.streams.delete(stream=stream)
    assert isinstance(result, DeleteResult)
    assert isinstance(result.commit_position, int)
    assert isinstance(result.prepare_position, int)

    with pytest.raises(Exception) as err:
        next(client.streams.read(stream=stream, count=20))

    assert "TODO: Stream not found" in str(err.value)


def test_delete_stream_with_revision(client):
    stream = str(uuid.uuid4())
    for i in range(3):
        client.streams.append(stream=stream, event_type="foobar", data=f"{i}".encode())

    assert len(list(client.streams.read(stream=stream, count=20))) == 3

    # TODO: this should be a custom exception
    with pytest.raises(grpc._channel._InactiveRpcError) as err:
        client.streams.delete(stream=stream, revision=1)

    assert "Expected version: 1, Actual version: 2" in str(err.value)
    client.streams.delete(stream=stream, revision=2)
