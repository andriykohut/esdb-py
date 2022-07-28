import uuid

import grpc
import pytest

from esdb.client.client import AsyncESClient
from tests.conftest import root_cert


@pytest.mark.asyncio
async def test_read_and_write_stream_with_tls_and_basic_auth(async_client_tls):
    stream = str(uuid.uuid4())
    for _ in range(10):
        await async_client_tls.streams.append(stream=stream, event_type="foobar", data={})

    events = []
    async for event in async_client_tls.streams.read(stream=stream, count=500):
        events.append(event)
    assert len(list(events)) == 10


@pytest.mark.asyncio
async def test_invalid_cert():
    client = AsyncESClient("localhost:2111", root_certificates=b"foo", username="admin", password="changeit")
    with pytest.raises(grpc.aio._call.AioRpcError):
        await client.streams.append("foo", "test_event", b"data")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["user", "password"],
    (
        ("admin", "foobar"),
        ("foobar", "changeit"),
    ),
)
async def test_invalid_user_pass(user, password):
    client = AsyncESClient("localhost:2111", root_certificates=root_cert(), username=user, password=password)
    with pytest.raises(grpc.aio._call.AioRpcError) as err:
        await client.streams.append("foo", "test_event", b"data")

    assert "UNAUTHENTICATED" in str(err.value)
