import grpc
import pytest

from esdb import ESClient
from esdb.exceptions import DiscoveryError
from esdb.gossip import Gossip


@pytest.mark.asyncio
async def test_invalid_cert():
    client = ESClient("esdb://admin:changeit@localhost:2111", root_certificates=b"")
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
    client = ESClient(f"esdb://{user}:{password}@localhost:2111?tlscafile=certs/ca/ca.crt")
    async with client.connect() as conn:
        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            await conn.streams.append("foo", "test_event", b"data")

    assert "UNAUTHENTICATED" in str(err.value)


@pytest.mark.asyncio
async def test_discovery_failed(monkeypatch):
    client = ESClient(
        f"esdb+discover://admin:changeit@localhost:2111?discoveryinterval=0&maxdiscoverattempts=3&tlscafile=certs/ca/ca.crt"
    )

    async def _get_members(*_):
        return []

    monkeypatch.setattr(Gossip, "get_members", _get_members)
    with pytest.raises(DiscoveryError) as err:
        async with client.connect():
            ...

    assert str(err.value) == "Discovery failed after 3 attempt(s)"
