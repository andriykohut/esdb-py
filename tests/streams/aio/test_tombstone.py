import uuid

import grpc
import pytest

from client.streams.base import TombstoneResult


@pytest.mark.asyncio
async def test_tombstone(async_client):
    stream = str(uuid.uuid4())
    await async_client.streams.append(stream=stream, event_type="foo", data=b"")
    result = await async_client.streams.tombstone(stream=stream)
    assert isinstance(result, TombstoneResult)
    assert result.commit_position > 0
    assert result.prepare_position > 0
    # TODO: This should be a custom exception
    with pytest.raises(grpc.aio._call.AioRpcError) as err:
        async for _ in async_client.streams.read(stream=stream, count=20):
            ...

    assert f"Event stream '{stream}' is deleted." in str(err.value)

    # TODO: This should be a custom exception
    with pytest.raises(grpc.aio._call.AioRpcError) as err:
        await async_client.streams.append(stream=stream, event_type="foo", data=b"")

    assert f"Event stream '{stream}' is deleted." in str(err.value)
