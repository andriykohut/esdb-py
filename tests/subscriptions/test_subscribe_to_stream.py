import threading
import time
import uuid

import grpc
import pytest


def test_create_subscription(client):
    stream = f"stream-{str(uuid.uuid4())}"
    group = f"group-{str(uuid.uuid4())}"

    responses = []

    for _ in range(10):
        with threading.Lock():
            client.streams.append(stream, "foobar", b"data")

    client.subscriptions.create_stream_subscription(stream=stream, group_name=group, revision=1)

    deadline = time.time() + 3

    def handler(response, reader):
        responses.append(response)
        if len(responses) == 10:
            reader.cancel()
        if time.time() >= deadline:
            pytest.fail("Deadline exceeded")

    with pytest.raises(grpc._channel._MultiThreadedRendezvous) as err:
        client.subscriptions.subscribe_to_stream(stream, group, handler)

    assert "Locally cancelled by application!" in str(err.value)

    assert len(responses) == 10
