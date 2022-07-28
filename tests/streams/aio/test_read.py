import uuid
from unittest.mock import ANY

import pytest

from esdb.client.streams.base import ReadResult


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["data", "expected_content_type"],
    (
        (b"some bytes", "application/octet-stream"),
        ({"foo": "bar"}, "application/json"),
    ),
)
async def test_append_and_read(data, async_client, expected_content_type):
    stream = str(uuid.uuid4())
    await async_client.streams.append(
        stream=stream, event_type="foobar", data=data, custom_metadata={"raisedBy": "me"}
    )
    [response] = [e async for e in async_client.streams.read(stream=stream, count=1)]

    assert isinstance(response, ReadResult)
    assert response.data == data
    assert response.commit_position == 0
    assert response.prepare_position == 0
    assert isinstance(response.id, str)
    assert response.metadata == {"created": ANY, "content-type": expected_content_type, "type": "foobar"}
    assert response.stream_name == stream
    assert response.custom_metadata == {"raisedBy": "me"}


@pytest.mark.asyncio
async def test_read_count(async_client):
    stream = str(uuid.uuid4())
    for i in range(20):
        await async_client.streams.append(stream=stream, event_type="foobar", data={"i": i})

    expected_events = list(range(20))
    reversed_events = list(reversed(expected_events))

    all_events = [e async for e in async_client.streams.read(stream=stream, count=20)]
    all_events_backwards = [e async for e in async_client.streams.read(stream=stream, count=20, backwards=True)]
    first_ten = [e async for e in async_client.streams.read(stream=stream, count=10)]
    first_ten_backwards = [e async for e in async_client.streams.read(stream=stream, count=10, backwards=True)]
    last_ten = [e async for e in async_client.streams.read(stream=stream, count=10, revision=10)]
    last_ten_backwards = [
        e async for e in async_client.streams.read(stream=stream, count=10, revision=9, backwards=True)
    ]

    assert len(all_events) == 20
    assert [e.data["i"] for e in all_events] == expected_events

    assert len(all_events_backwards) == 20
    assert [e.data["i"] for e in all_events_backwards] == reversed_events

    assert len(first_ten) == 10
    assert [e.data["i"] for e in first_ten] == expected_events[:10]

    assert len(first_ten_backwards) == 10
    assert [e.data["i"] for e in first_ten_backwards] == reversed_events[:10]

    assert len(last_ten) == 10
    assert [e.data["i"] for e in last_ten] == expected_events[10:]

    assert len(last_ten_backwards) == 10
    assert [e.data["i"] for e in last_ten_backwards] == reversed_events[10:]


@pytest.mark.asyncio
async def test_read_from_projection(async_client):
    event_type = str(uuid.uuid4())
    for _ in range(10):
        await async_client.streams.append(stream=str(uuid.uuid4()), event_type=event_type, data={})

    events = [e async for e in async_client.streams.read(stream=f"$et-{event_type}", count=500)]
    assert events
    assert all(e.metadata["type"] == event_type for e in events)