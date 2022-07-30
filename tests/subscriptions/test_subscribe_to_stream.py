import queue
import threading
import time
import uuid
from collections import defaultdict
from unittest import mock

import pytest

from esdb.client.subscriptions import SubscriptionSettings
from esdb.client.subscriptions.base import Event


def test_subscribe_to_stream(client):
    stream = f"stream-{str(uuid.uuid4())}"
    group = f"group-{str(uuid.uuid4())}"

    with client.connect() as conn:
        # emit some events to the same stream
        for _ in range(10):
            conn.streams.append(stream, "foobar", b"data")

        # create a subscription
        conn.subscriptions.create_stream_subscription(
            stream=stream,
            group_name=group,
            settings=SubscriptionSettings(
                read_batch_size=5,
                live_buffer_size=10,
                history_buffer_size=10,
                checkpoint=SubscriptionSettings.DurationType(
                    type=SubscriptionSettings.DurationType.Type.MS,
                    value=10000,
                ),
            ),
        )

    # wait for 10 responses or stop after 3 seconds
    with client.connect() as conn:
        deadline = time.time() + 3
        events = []
        subscription = conn.subscriptions.subscribe_to_stream(stream=stream, group_name=group, buffer_size=10)
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


def test_multiple_consumers(client):
    stream = f"stream-{str(uuid.uuid4())}"
    group = f"group-{str(uuid.uuid4())}"

    with client.connect() as conn:
        # emit some events to the same stream
        for i in range(50):
            conn.streams.append(stream, "foobar", {"i": i})

        # create a subscription
        conn.subscriptions.create_stream_subscription(
            stream=stream,
            group_name=group,
            settings=SubscriptionSettings(
                max_subscriber_count=50,
                read_batch_size=5,
                live_buffer_size=10,
                history_buffer_size=10,
                consumer_strategy=SubscriptionSettings.ConsumerStrategy.ROUND_ROBIN,
                checkpoint=SubscriptionSettings.DurationType(
                    type=SubscriptionSettings.DurationType.Type.MS,
                    value=10000,
                ),
            ),
        )

    result_queues = [queue.Queue(), queue.Queue(), queue.Queue()]

    def run_consumer(num: int, q: queue.SimpleQueue):
        with client.connect() as conn:
            subscription = conn.subscriptions.subscribe_to_stream(stream=stream, group_name=group, buffer_size=5)
            for event in subscription:
                q.put((num, event.data["i"]))
                subscription.ack([event])

    # Spawn multiple consumers
    for idx, q in enumerate(result_queues):
        threading.Thread(target=lambda: run_consumer(idx, q), daemon=True).start()

    count = 0
    result = defaultdict(list)

    while True:
        if count == 50:
            break
        for q in result_queues:
            try:
                num, data = q.get_nowait()
                count += 1
                result[num].append(data)
            except queue.Empty:
                ...

    all_jobs = []
    for worker, results in result.items():
        # ensure all threads consumed events
        assert len(results) > 0
        all_jobs.extend(results)

    # ensure all events were processed
    assert len(all_jobs) == 50
    assert sorted(all_jobs) == list(range(50))
