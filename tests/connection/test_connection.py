import grpc
import pytest

from esdb import ESClient
from esdb.client import Preference
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
        ESClient(endpoint="...", username=user, password=password)

    assert str(err.value) == "Both username and password are required"
