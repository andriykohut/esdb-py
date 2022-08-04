import asyncio
import itertools
import time
import uuid
from collections import defaultdict
from unittest import mock

import pytest

from esdb.shared import Filter
from esdb.subscriptions import Event, NackAction, SubscriptionSettings


@pytest.mark.asyncio
async def test_create_stream_subscription(client, wait_for_stream):
    stream = str(uuid.uuid4())
    async with client.connect() as conn:
        await conn.streams.append(
            stream=str(uuid.uuid4()),
            event_type="some_event",
            data={},
        )

        # await wait_for_stream(conn, stream)

        await conn.subscriptions.create_stream_subscription(
            stream=stream,
            group_name="me",
            settings=SubscriptionSettings(
                live_buffer_size=15,
                read_batch_size=10,
                history_buffer_size=15,
                checkpoint=SubscriptionSettings.DurationType(
                    type=SubscriptionSettings.DurationType.Type.TICKS,
                    value=1000,
                ),
                resolve_links=False,
                extra_statistics=True,
                max_retry_count=5,
                min_checkpoint_count=20,
                max_checkpoint_count=30,
                max_subscriber_count=10,
                message_timeout=SubscriptionSettings.DurationType(
                    type=SubscriptionSettings.DurationType.Type.MS,
                    value=1000,
                ),
                consumer_strategy=SubscriptionSettings.ConsumerStrategy.ROUND_ROBIN,
            ),
        )


@pytest.mark.asyncio
async def test_subscribe_to_stream(client):
    stream = f"stream-{str(uuid.uuid4())}"
    group = f"group-{str(uuid.uuid4())}"

    async with client.connect() as conn:
        # emit some events to the same stream
        for _ in range(10):
            await conn.streams.append(stream, "foobar", b"data")

        # create a subscription
        await conn.subscriptions.create_stream_subscription(
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
    async with client.connect() as conn:
        deadline = time.time() + 3
        events = []
        subscription = conn.subscriptions.subscribe(stream=stream, group_name=group, buffer_size=10)
        async for event in subscription:
            events.append(event)
            await subscription.ack([event])
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


@pytest.mark.asyncio
async def test_multiple_consumers(client):
    stream = f"stream-{str(uuid.uuid4())}"
    group = f"group-{str(uuid.uuid4())}"

    async with client.connect() as conn:
        # emit some events to the same stream
        for i in range(50):
            await conn.streams.append(stream, "foobar", {"i": i})

        # create a subscription
        await conn.subscriptions.create_stream_subscription(
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

    result_queue = asyncio.Queue()

    async def run_consumer(id: int):
        async with client.connect() as conn:
            subscription = conn.subscriptions.subscribe(stream=stream, group_name=group, buffer_size=5)
            async for event in subscription:
                await subscription.ack([event])
                await result_queue.put((id, event.data["i"]))
                if result_queue.qsize() == 50:
                    raise Exception("I'm done")

    try:
        await asyncio.gather(
            run_consumer(1),
            run_consumer(2),
            run_consumer(3),
            return_exceptions=False,
        )
    except Exception:
        ...

    results_by_consumer = defaultdict(list)

    while not result_queue.empty():
        consumer, evt_num = await result_queue.get()
        results_by_consumer[consumer].append(evt_num)

    for events in results_by_consumer.values():
        # ensure each consume did some work
        assert events

    all_events = list(itertools.chain.from_iterable(results_by_consumer.values()))
    assert sorted(all_events) == list(range(50))


@pytest.mark.asyncio
async def test_nack(client):
    stream = f"stream-{str(uuid.uuid4())}"
    group = f"group-{str(uuid.uuid4())}"

    async with client.connect() as conn:
        # emit some events to the same stream
        for i in range(10):
            await conn.streams.append(stream, "foobar", {"i": i})

        # create a subscription
        await conn.subscriptions.create_stream_subscription(
            stream=stream,
            group_name=group,
            settings=SubscriptionSettings(
                read_batch_size=50,
                live_buffer_size=100,
                history_buffer_size=100,
                max_retry_count=2,
                checkpoint=SubscriptionSettings.DurationType(
                    type=SubscriptionSettings.DurationType.Type.MS,
                    value=10000,
                ),
            ),
        )

    # wait for 10 responses or stop after 3 seconds
    expected_count = 10 * 2  # number of events * retry count
    count = 0
    async with client.connect() as conn:
        deadline = time.time() + 3
        subscription = conn.subscriptions.subscribe(stream=stream, group_name=group, buffer_size=100)
        async for event in subscription:
            count += 1
            await subscription.nack([event], NackAction.RETRY)
            if time.time() >= deadline:
                pytest.fail("Didn't read all events")
            if count == expected_count:
                break


@pytest.mark.asyncio
async def test_create_all_subscription(client):
    event_type = str(uuid.uuid4())
    group_name = str(uuid.uuid4())
    async with client.connect() as conn:
        for _ in range(10):
            await conn.streams.append(stream=str(uuid.uuid4()), event_type=event_type, data=b"")
        await conn.subscriptions.create_all_subscription(
            group_name=group_name,
            filter_by=Filter(kind=Filter.Kind.EVENT_TYPE, regex=f"^{event_type}$", checkpoint_interval_multiplier=200),
            settings=SubscriptionSettings(
                read_batch_size=50,
                live_buffer_size=100,
                history_buffer_size=100,
                max_retry_count=2,
                checkpoint=SubscriptionSettings.DurationType(
                    type=SubscriptionSettings.DurationType.Type.MS,
                    value=10000,
                ),
            ),
        )

        events = []
        async for event in conn.subscriptions.subscribe(group_name=group_name, buffer_size=10):
            events.append(event)
            if len(events) == 10:
                break

        assert events
        assert all(e.type == event_type for e in events)
