import uuid

import pytest

from client.streams.base import Message, StreamState


def test_batch_append(client):
    stream = str(uuid.uuid4())
    messages: list[Message] = [
        Message(event_type="one", data={"item": 1}),
        Message(event_type="one", data={"item": 2}),
        Message(event_type="one", data={"item": 3}),
        Message(event_type="two", data={"item": 1}),
        Message(event_type="two", data={"item": 2}),
        Message(event_type="two", data={"item": 3}),
    ]
    client.streams.batch_append(stream=stream, messages=messages)
    events = list(client.streams.read(stream=stream, count=50))
    assert len(events) == 6
    assert len([e for e in events if e.metadata["type"] == "one"]) == 3
    assert len([e for e in events if e.metadata["type"] == "two"]) == 3


def test_batch_append_to_unknown_stream_expecting_it_exists(client):
    stream = str(uuid.uuid4())
    messages = [Message(event_type="foo", data=b"") for _ in range(3)]
    with pytest.raises(Exception) as err:
        client.streams.batch_append(stream, messages, stream_state=StreamState.STREAM_EXISTS)

    assert 'message: "WrongExpectedVersion"' in str(err.value)


def test_batch_append_deadline(client):
    stream = str(uuid.uuid4())
    messages = [Message(event_type="foo", data=b"") for _ in range(3)]
    with pytest.raises(Exception) as err:
        client.streams.batch_append(stream, messages, deadline_ms=0)

    assert "TODO: got error code: DEADLINE_EXCEEDED" in str(err.value)
