import time
import uuid

import grpc
import pytest


def test_subscribe_to_stream(client):
    stream = f"stream-{str(uuid.uuid4())}"
    group = f"group-{str(uuid.uuid4())}"

    responses = []

    # emit some events to the same stream
    for _ in range(10):
        client.streams.append(stream, "foobar", b"data")

    # create a subscription
    client.subscriptions.create_stream_subscription(stream=stream, group_name=group, revision=1)

    deadline = time.time() + 3

    # wait for 10 responses or stop after 3 seconds
    def handler(response, reader):
        responses.append(response)
        if len(responses) == 10:
            reader.cancel()
        if time.time() >= deadline:
            reader.cancel()
            pytest.fail("Deadline exceeded")

    with pytest.raises(grpc._channel._MultiThreadedRendezvous) as err:
        client.subscriptions.subscribe_to_stream(stream, group, handler)

    assert "Locally cancelled by application!" in str(err.value)

    assert len(responses) == 10
