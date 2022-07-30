import uuid

import grpc
import pytest

from esdb.client.streams.base import TombstoneResult


def test_tombstone(client):
    stream = str(uuid.uuid4())
    with client.connect() as conn:
        conn.streams.append(stream=stream, event_type="foo", data=b"")
        result = conn.streams.tombstone(stream=stream)
        assert isinstance(result, TombstoneResult)
        assert result.commit_position > 0
        assert result.prepare_position > 0
        with pytest.raises(grpc._channel._MultiThreadedRendezvous) as err:
            next(conn.streams.read(stream=stream, count=20))

        assert f"Event stream '{stream}' is deleted." in str(err.value)

        with pytest.raises(grpc._channel._InactiveRpcError) as err:
            conn.streams.append(stream=stream, event_type="foo", data=b"")

        assert f"Event stream '{stream}' is deleted." in str(err.value)
