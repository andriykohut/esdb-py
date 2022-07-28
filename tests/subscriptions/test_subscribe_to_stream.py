import time
import uuid
from unittest import mock

import pytest

from esdb.client.subscriptions.base import Event


def test_subscribe_to_stream(client):
    stream = f"stream-{str(uuid.uuid4())}"
    group = f"group-{str(uuid.uuid4())}"

    # emit some events to the same stream
    for _ in range(10):
        client.streams.append(stream, "foobar", b"data")

    # create a subscription
    client.subscriptions.create_stream_subscription(stream=stream, group_name=group)

    # wait for 10 responses or stop after 3 seconds
    deadline = time.time() + 3
    events = []
    subscription = client.subscriptions.subscribe_to_stream(stream, group)
    for event in subscription:
        events.append(event)
        subscription.ack([event])
        if time.time() >= deadline:
            pytest.fail("Didn't read all events")
        if len(events) == 10:
            break

    for evt in events:
        assert isinstance(evt, Event)
        assert evt.stream == stream
        assert evt.data == b"data"
        assert evt.type == "foobar"
        assert evt.metadata == {
            "content-type": "application/octet-stream",
            "type": "foobar",
            "created": mock.ANY,
        }
