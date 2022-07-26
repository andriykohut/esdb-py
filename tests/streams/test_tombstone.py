import uuid

import grpc
import pytest

from streams import TombstoneResult


def test_tombstone(client):
    stream = str(uuid.uuid4())
    client.streams.append(stream=stream, event_type="foo", data=b"")
    result = client.streams.tombstone(stream=stream)
    assert isinstance(result, TombstoneResult)
    assert result.commit_position > 0
    assert result.prepare_position > 0
    # TODO: This should be a custom exception
    with pytest.raises(grpc._channel._MultiThreadedRendezvous) as err:
        next(client.streams.read(stream=stream, count=20))

    assert f"Event stream '{stream}' is deleted." in str(err.value)

    # TODO: This should be a custom exception
    with pytest.raises(grpc._channel._InactiveRpcError) as err:
        client.streams.append(stream=stream, event_type="foo", data=b"")

    assert f"Event stream '{stream}' is deleted." in str(err.value)
