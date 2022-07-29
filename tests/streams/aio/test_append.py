import datetime
import uuid

import pytest

from esdb.client.streams.base import AppendResult, StreamState


@pytest.mark.asyncio
async def test_appending_to_unknown_stream_with_stream_exists_state(async_client):
    now = datetime.datetime.utcnow().isoformat()
    async with async_client.connect() as conn:
        with pytest.raises(Exception) as e:
            await conn.streams.append(
                stream=str(uuid.uuid4()),
                event_type="test_event",
                data={"now": now},
                stream_state=StreamState.STREAM_EXISTS,
            )

    assert "TODO: wrong expected version" in str(e.value)


@pytest.mark.parametrize("stream_state", [StreamState.NO_STREAM, StreamState.ANY])
@pytest.mark.asyncio
async def test_appending_to_unknown_stream(async_client, stream_state):
    now = datetime.datetime.utcnow().isoformat()
    async with async_client.connect() as conn:
        result = await conn.streams.append(
            stream=str(uuid.uuid4()),
            event_type="test_event",
            data={"now": now},
            stream_state=stream_state,
        )

    assert isinstance(result, AppendResult)


@pytest.mark.parametrize("data", [b"some bytes", {"x": 1, "y": 2}])
@pytest.mark.asyncio
async def test_appending_content_types(async_client, data):
    async with async_client.connect() as conn:
        result = await conn.streams.append(stream=str(uuid.uuid4()), event_type="test_event", data=data)
    assert isinstance(result, AppendResult)


@pytest.mark.asyncio
async def test_appending_at_wrong_revision(async_client):
    # initialize stream
    stream = str(uuid.uuid4())
    async with async_client.connect() as conn:
        await conn.streams.append(stream=stream, event_type="test_event", data=b"")

        # try to append at unknown position
        with pytest.raises(Exception) as e:
            await conn.streams.append(
                stream=stream,
                event_type="test_event",
                data=b"",
                revision=100,
            )

        assert "TODO: wrong expected version" in str(e)


@pytest.mark.asyncio
async def test_appending_at_correct_revision(async_client):
    stream = str(uuid.uuid4())
    async with async_client.connect() as conn:
        # Publish 0th event
        await conn.streams.append(stream=stream, event_type="test_event", data=b"")
        # Publish 1th event
        await conn.streams.append(stream=stream, event_type="test_event", data=b"")
        # Publishing from 1th should work
        await conn.streams.append(stream=stream, event_type="test_event", data=b"", revision=1)
