import datetime
import uuid

import pytest

from esdb.client.streams.base import AppendResult, StreamState


def test_appending_to_unknown_stream_with_stream_exists_state(client):
    now = datetime.datetime.utcnow().isoformat()
    with client.connect() as conn:
        with pytest.raises(Exception) as e:
            conn.streams.append(
                stream=str(uuid.uuid4()),
                event_type="test_event",
                data={"now": now},
                stream_state=StreamState.STREAM_EXISTS,
            )

    assert "TODO: wrong expected version" in str(e.value)


@pytest.mark.parametrize("stream_state", [StreamState.NO_STREAM, StreamState.ANY])
def test_appending_to_unknown_stream(client, stream_state):
    now = datetime.datetime.utcnow().isoformat()
    with client.connect() as conn:
        result = conn.streams.append(
            stream=str(uuid.uuid4()),
            event_type="test_event",
            data={"now": now},
            stream_state=stream_state,
        )

    assert isinstance(result, AppendResult)


@pytest.mark.parametrize("data", [b"some bytes", {"x": 1, "y": 2}])
def test_appending_content_types(client, data):
    with client.connect() as conn:
        result = conn.streams.append(stream=str(uuid.uuid4()), event_type="test_event", data=data)

    assert isinstance(result, AppendResult)


def test_appending_at_wrong_revision(client):
    # initialize stream
    stream = str(uuid.uuid4())
    with client.connect() as conn:
        conn.streams.append(
            stream=stream,
            event_type="test_event",
            data=b"",
        )

        # try to append at unknown position
        with pytest.raises(Exception) as e:
            conn.streams.append(
                stream=stream,
                event_type="test_event",
                data=b"",
                revision=100,
            )

    assert "TODO: wrong expected version" in str(e)


def test_appending_at_correct_revision(client):
    stream = str(uuid.uuid4())
    with client.connect() as conn:
        # Publish first event
        conn.streams.append(
            stream=stream,
            event_type="test_event",
            data=b"",
        )
        # Publish second event
        conn.streams.append(
            stream=stream,
            event_type="test_event",
            data=b"",
        )

        # Publishing from second should work
        conn.streams.append(
            stream=stream,
            event_type="test_event",
            data=b"",
            revision=1,
        )
