import grpc
import pytest

from esdb import ESClient
from esdb.exceptions import DiscoveryError
from esdb.gossip import Gossip
from tests.conftest import root_cert


@pytest.mark.asyncio
async def test_invalid_cert():
    client = ESClient("localhost:2111", root_certificates=b"foo", username="admin", password="changeit")
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
    client = ESClient("localhost:2111", root_certificates=root_cert(), username=user, password=password)
    async with client.connect() as conn:
        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            await conn.streams.append("foo", "test_event", b"data")

    assert "UNAUTHENTICATED" in str(err.value)


@pytest.mark.parametrize(
    "user, password",
    [
        ("foo", None),
        (None, "foo"),
    ],
)
def test_missing_user_or_pass(user, password):
    with pytest.raises(ValueError) as err:
        ESClient(endpoints="...", username=user, password=password)

    assert str(err.value) == "Both username and password are required"


@pytest.mark.asyncio
async def test_discovery_failed(client, monkeypatch):
    client.discovery_interval = 0
    client.discovery_attempts = 3

    async def _get_members(*_):
        return []

    monkeypatch.setattr(Gossip, "get_members", _get_members)
    with pytest.raises(DiscoveryError) as err:
        async with client.connect():
            ...

    assert str(err.value) == "Discovery failed after 3 attempt(s)"
