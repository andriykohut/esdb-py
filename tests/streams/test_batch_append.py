import uuid

import pytest

from esdb.client.exceptions import ClientException
from esdb.client.streams import Message, StreamState


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
    with client.connect() as conn:
        conn.streams.batch_append(stream=stream, messages=messages)
        events = list(conn.streams.read(stream=stream, count=50))
    assert len(events) == 6
    assert len([e for e in events if e.metadata["type"] == "one"]) == 3
    assert len([e for e in events if e.metadata["type"] == "two"]) == 3


def test_batch_append_to_unknown_stream_expecting_it_exists(client):
    stream = str(uuid.uuid4())
    messages = [Message(event_type="foo", data=b"") for _ in range(3)]
    with client.connect() as conn:
        with pytest.raises(ClientException) as err:
            conn.streams.batch_append(stream, messages, stream_state=StreamState.STREAM_EXISTS)

    assert "Append failed with WrongExpectedVersion and code 6" in str(err.value)


def test_batch_append_deadline(client):
    stream = str(uuid.uuid4())
    messages = [Message(event_type="foo", data=b"") for _ in range(3)]
    with client.connect() as conn:
        with pytest.raises(ClientException) as err:
            conn.streams.batch_append(stream, messages, deadline_ms=0)

    assert "Append failed with Timeout" in str(err.value)
