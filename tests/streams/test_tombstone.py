import uuid

import grpc
import pytest

from esdb.streams.types import TombstoneResult


@pytest.mark.asyncio
async def test_tombstone(client):
    stream = str(uuid.uuid4())
    async with client.connect() as conn:
        await conn.streams.append(stream=stream, event_type="foo", data=b"")
        result = await conn.streams.tombstone(stream=stream)
        assert isinstance(result, TombstoneResult)
        assert result.commit_position > 0
        assert result.prepare_position > 0
        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            async for _ in conn.streams.read(stream=stream, count=20):
                ...

        assert f"Event stream '{stream}' is deleted." in str(err.value)

        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            await conn.streams.append(stream=stream, event_type="foo", data=b"")

        assert f"Event stream '{stream}' is deleted." in str(err.value)


@pytest.mark.asyncio
async def test_tombstone_with_revision(client):
    stream = str(uuid.uuid4())
    async with client.connect() as conn:
        await conn.streams.append(stream=stream, event_type="foo", data=b"")
        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            await conn.streams.tombstone(stream=stream, revision=23)

        assert "Expected version: 23, Actual version: 0" in str(err.value)

        await conn.streams.tombstone(stream=stream, revision=0)
