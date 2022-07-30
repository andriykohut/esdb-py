import uuid

import grpc
import pytest

from esdb.client.exceptions import StreamNotFound
from esdb.client.streams import StreamState
from esdb.client.streams.base import DeleteResult


@pytest.mark.asyncio
async def test_delete_stream(async_client):
    stream = str(uuid.uuid4())
    async with async_client.connect() as conn:
        await conn.streams.append(stream=stream, event_type="foobar", data=b"a")
        await conn.streams.append(stream=stream, event_type="foobar", data=b"b")

        assert len([e async for e in conn.streams.read(stream=stream, count=20)]) == 2

        result = await conn.streams.delete(stream=stream)
        assert isinstance(result, DeleteResult)
        assert isinstance(result.commit_position, int)
        assert isinstance(result.prepare_position, int)

        with pytest.raises(StreamNotFound) as err:
            async for _ in conn.streams.read(stream=stream, count=20):
                ...

        assert str(err.value) == f"Stream '{stream}' not found"


@pytest.mark.asyncio
async def test_delete_stream_with_revision(async_client):
    stream = str(uuid.uuid4())
    async with async_client.connect() as conn:
        for i in range(3):
            await conn.streams.append(stream=stream, event_type="foobar", data=f"{i}".encode())

        assert len([e async for e in conn.streams.read(stream=stream, count=20)]) == 3

        # TODO: this should be a custom exception
        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            await conn.streams.delete(stream=stream, revision=1)

        assert "Expected version: 1, Actual version: 2" in str(err.value)
        await conn.streams.delete(stream=stream, revision=2)


@pytest.mark.asyncio
async def test_delete_with_stream_state(async_client):
    stream1 = str(uuid.uuid4())
    stream2 = str(uuid.uuid4())
    stream3 = str(uuid.uuid4())
    async with async_client.connect() as conn:
        await conn.streams.append(stream=stream1, event_type="foobar", data=b"")
        await conn.streams.append(stream=stream2, event_type="foobar", data=b"")

        await conn.streams.delete(stream=stream1, stream_state=StreamState.STREAM_EXISTS)
        # TODO: this should be a custom exception
        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            await conn.streams.delete(stream=stream2, stream_state=StreamState.NO_STREAM)

        assert "Expected version: -1, Actual version: 0" in str(err)

        with pytest.raises(grpc.aio._call.AioRpcError):
            # This doesn't make sense, since why would someone would delete stream if they think it doesn't exist?
            await conn.streams.delete(stream=stream3, stream_state=StreamState.NO_STREAM)

        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            await conn.streams.delete(stream=stream3)

        assert "Expected version: -2, Actual version: -1" in str(err)
