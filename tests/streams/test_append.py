import datetime
import uuid

import pytest

from esdb.exceptions import WrongExpectedVersion
from esdb.streams import StreamState
from esdb.streams.types import AppendResult


@pytest.mark.asyncio
async def test_appending_to_unknown_stream_with_stream_exists_state(client):
    now = datetime.datetime.utcnow().isoformat()
    async with client.connect() as conn:
        with pytest.raises(WrongExpectedVersion) as e:
            await conn.streams.append(
                stream=str(uuid.uuid4()),
                event_type="test_event",
                data={"now": now},
                stream_state=StreamState.STREAM_EXISTS,
            )

    assert str(e.value) == "Expected state 'stream_exists', got 'no_stream'"


@pytest.mark.parametrize("stream_state", [StreamState.NO_STREAM, StreamState.ANY])
@pytest.mark.asyncio
async def test_appending_to_unknown_stream(client, stream_state):
    now = datetime.datetime.utcnow().isoformat()
    async with client.connect() as conn:
        result = await conn.streams.append(
            stream=str(uuid.uuid4()),
            event_type="test_event",
            data={"now": now},
            stream_state=stream_state,
        )

    assert isinstance(result, AppendResult)


@pytest.mark.parametrize("data", [b"some bytes", {"x": 1, "y": 2}])
@pytest.mark.asyncio
async def test_appending_content_types(client, data):
    async with client.connect() as conn:
        result = await conn.streams.append(stream=str(uuid.uuid4()), event_type="test_event", data=data)
    assert isinstance(result, AppendResult)


@pytest.mark.asyncio
async def test_appending_at_wrong_revision(client):
    # initialize stream
    stream = str(uuid.uuid4())
    async with client.connect() as conn:
        await conn.streams.append(stream=stream, event_type="test_event", data=b"")

        # try to append at unknown position
        with pytest.raises(WrongExpectedVersion) as e:
            await conn.streams.append(
                stream=stream,
                event_type="test_event",
                data=b"",
                revision=100,
            )

        assert str(e.value) == "Expected state 'revision=100', got 'revision=0'"


@pytest.mark.asyncio
async def test_appending_at_correct_revision(client):
    stream = str(uuid.uuid4())
    async with client.connect() as conn:
        # Publish 0th event
        await conn.streams.append(stream=stream, event_type="test_event", data=b"")
        # Publish 1th event
        await conn.streams.append(stream=stream, event_type="test_event", data=b"")
        # Publishing from 1th should work
        await conn.streams.append(stream=stream, event_type="test_event", data=b"", revision=1)
