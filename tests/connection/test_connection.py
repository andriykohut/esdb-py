import uuid

import grpc
import pytest

from esdb.client import ESClient
from tests.conftest import root_cert


def test_read_and_write_stream_with_tls_and_basic_auth(client_tls):
    stream = str(uuid.uuid4())
    with client_tls.connect() as conn:
        for _ in range(10):
            conn.streams.append(stream=stream, event_type="foobar", data={})

        events = list(conn.streams.read(stream=stream, count=500))

    assert len(events) == 10


def test_invalid_cert():
    client = ESClient("localhost:2111", root_certificates=b"foo", username="admin", password="changeit")
    with client.connect() as conn:
        with pytest.raises(grpc._channel._InactiveRpcError):
            conn.streams.append("foo", "test_event", b"data")


@pytest.mark.parametrize(
    ["user", "password"],
    (
        ("admin", "foobar"),
        ("foobar", "changeit"),
    ),
)
def test_invalid_user_pass(user, password):
    client = ESClient("localhost:2111", root_certificates=root_cert(), username=user, password=password)
    with client.connect() as conn:
        with pytest.raises(grpc._channel._InactiveRpcError) as err:
            conn.streams.append("foo", "test_event", b"data")

    assert "UNAUTHENTICATED" in str(err.value)
