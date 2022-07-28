import uuid

import pytest

from esdb.client.streams.base import BatchAppendResult, Message, StreamState


@pytest.mark.asyncio
async def test_batch_append(async_client):
    stream = str(uuid.uuid4())
    messages: list[Message] = [
        Message(event_type="one", data={"item": 1}),
        Message(event_type="one", data={"item": 2}),
        Message(event_type="one", data={"item": 3}),
        Message(event_type="two", data={"item": 1}),
        Message(event_type="two", data={"item": 2}),
        Message(event_type="two", data={"item": 3}),
    ]
    response = await async_client.streams.batch_append(stream=stream, messages=messages)
    assert isinstance(response, BatchAppendResult)
    events = [e async for e in async_client.streams.read(stream=stream, count=50)]
    assert len(events) == 6
    assert len([e for e in events if e.metadata["type"] == "one"]) == 3
    assert len([e for e in events if e.metadata["type"] == "two"]) == 3


@pytest.mark.asyncio
async def test_batch_append_to_unknown_stream_expecting_it_exists(async_client):
    stream = str(uuid.uuid4())
    messages = [Message(event_type="foo", data=b"") for _ in range(3)]
    with pytest.raises(Exception) as err:
        await async_client.streams.batch_append(stream, messages, stream_state=StreamState.STREAM_EXISTS)

    assert 'message: "WrongExpectedVersion"' in str(err.value)


@pytest.mark.asyncio
async def test_batch_append_deadline(async_client):
    stream = str(uuid.uuid4())
    messages = [Message(event_type="foo", data=b"") for _ in range(3)]
    with pytest.raises(Exception) as err:
        await async_client.streams.batch_append(stream, messages, deadline_ms=0)

    assert "TODO: got error code: DEADLINE_EXCEEDED" in str(err.value)