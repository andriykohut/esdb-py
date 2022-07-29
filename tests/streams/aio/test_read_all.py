import uuid

import pytest

from esdb.client.streams.base import Filter


@pytest.mark.asyncio
async def test_read_all_filter_by_event_type(async_client):
    event_type = str(uuid.uuid4())
    async with async_client.connect() as conn:
        for _ in range(20):
            await conn.streams.append(
                stream=str(uuid.uuid4()),
                event_type=event_type,
                data=b"",
            )

        events = [
            evt
            async for evt in conn.streams.read_all(
                count=500,
                filter_by=Filter(
                    kind=Filter.Kind.EVENT_TYPE,
                    regex=event_type,
                ),
            )
        ]

        assert len(events) == 20
        assert all(e.event_type == event_type for e in events)


@pytest.mark.asyncio
async def test_read_all_filter_by_stream_name(async_client):
    stream_prefix = str(uuid.uuid4())
    async with async_client.connect() as conn:
        for i in range(20):
            await conn.streams.append(
                stream=f"{stream_prefix}-{i}",
                event_type="i-dont-care",
                data=b"",
            )

        events = [
            evt
            async for evt in conn.streams.read_all(
                count=500,
                filter_by=Filter(
                    kind=Filter.Kind.STREAM,
                    regex=stream_prefix,
                ),
            )
        ]
        assert len(events) == 20
        assert all(e.stream_name.startswith(stream_prefix) for e in events)
