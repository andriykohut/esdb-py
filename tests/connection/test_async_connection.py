import uuid

import grpc
import pytest

from esdb.client import AsyncESClient
from tests.conftest import root_cert


@pytest.mark.asyncio
async def test_read_and_write_stream_with_tls_and_basic_auth(async_client_tls):
    stream = str(uuid.uuid4())
    events = []
    async with async_client_tls.connect() as conn:
        for _ in range(10):
            await conn.streams.append(stream=stream, event_type="foobar", data={})
        async for event in conn.streams.read(stream=stream, count=500):
            events.append(event)
    assert len(list(events)) == 10


@pytest.mark.asyncio
async def test_invalid_cert():
    client = AsyncESClient("localhost:2111", root_certificates=b"foo", username="admin", password="changeit")
    async with client.connect() as conn:
        with pytest.raises(grpc.aio._call.AioRpcError):
            await conn.streams.append("foo", "test_event", b"data")


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
    async with client.connect() as conn:
        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            await conn.streams.append("foo", "test_event", b"data")

    assert "UNAUTHENTICATED" in str(err.value)
