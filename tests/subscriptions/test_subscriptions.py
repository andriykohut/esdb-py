import asyncio
import itertools
import time
import uuid
from collections import defaultdict
from unittest import mock

import grpc
import pytest

from esdb.shared import Filter
from esdb.subscriptions import Event, NackAction, SubscriptionSettings


@pytest.mark.asyncio
async def test_create_and_update_stream_subscription(client):
    stream = str(uuid.uuid4())
    async with client.connect() as conn:
        await conn.streams.append(
            stream=str(uuid.uuid4()),
            event_type="some_event",
            data={},
        )

        await conn.subscriptions.create_stream_subscription(
            stream=stream,
            group_name="me",
            settings=SubscriptionSettings(
                live_buffer_size=15,
                read_batch_size=10,
                history_buffer_size=15,
                checkpoint_ms=10000,
                resolve_links=False,
                extra_statistics=True,
                max_retry_count=5,
                min_checkpoint_count=20,
                max_checkpoint_count=30,
                max_subscriber_count=10,
                message_timeout_ms=10000,
                consumer_strategy=SubscriptionSettings.ConsumerStrategy.ROUND_ROBIN,
            ),
        )

        info = await conn.subscriptions.get_info(group_name="me", stream=stream)
        assert info.group_name == "me"
        assert info.consumer_strategy == "RoundRobin"

        await conn.subscriptions.update_stream_subscription(
            stream=stream,
            group_name="me",
            settings=SubscriptionSettings(
                live_buffer_size=15,
                read_batch_size=10,
                history_buffer_size=15,
                consumer_strategy=SubscriptionSettings.ConsumerStrategy.DISPATCH_TO_SINGLE,
                checkpoint_ms=10000,
            ),
        )

        info = await conn.subscriptions.get_info(group_name="me", stream=stream)
        assert info.group_name == "me"
        assert info.consumer_strategy == "DispatchToSingle"


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
                checkpoint_ms=10000,
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
                checkpoint_ms=100000,
                message_timeout_ms=10000,
                max_checkpoint_count=1,
                min_checkpoint_count=1,
            ),
        )

    result_queue = asyncio.Queue()

    async def run_consumer(id: int):
        async with client.connect() as conn:
            subscription = conn.subscriptions.subscribe(stream=stream, group_name=group, buffer_size=1)
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
                checkpoint_ms=10000,
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
async def test_create_and_update_all_subscription(client):
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
                checkpoint_ms=100000,
            ),
        )

        events = []
        async for event in conn.subscriptions.subscribe(group_name=group_name, buffer_size=10):
            events.append(event)
            if len(events) == 10:
                break

        assert events
        assert all(e.type == event_type for e in events)

        await conn.subscriptions.update_all_subscription(
            group_name=group_name,
            settings=SubscriptionSettings(
                read_batch_size=50,
                live_buffer_size=100,
                history_buffer_size=100,
                max_retry_count=5,
                checkpoint_ms=100000,
            ),
        )

        info = await conn.subscriptions.get_info(group_name=group_name)
        assert info.consumer_strategy == "DispatchToSingle"
        assert info.max_retry_count == 5


@pytest.mark.asyncio
async def test_delete_stream_subscription(client):
    stream = str(uuid.uuid4())
    group_name = str(uuid.uuid4())
    async with client.connect() as conn:
        await conn.streams.append(stream=str(uuid.uuid4()), event_type="some_event", data={})
        await conn.subscriptions.create_stream_subscription(
            stream=stream,
            group_name=group_name,
            settings=SubscriptionSettings(
                live_buffer_size=15,
                read_batch_size=10,
                history_buffer_size=15,
                checkpoint_ms=10000,
            ),
        )

        info = await conn.subscriptions.get_info(group_name, stream)
        assert info.group_name == group_name

        await conn.subscriptions.delete(group_name, stream)
        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            await conn.subscriptions.get_info(group_name, stream)
        assert err.value.code() == grpc.StatusCode.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_all_subscription(client):
    group_name = str(uuid.uuid4())
    async with client.connect() as conn:
        await conn.subscriptions.create_all_subscription(
            group_name=group_name,
            filter_by=Filter(kind=Filter.Kind.EVENT_TYPE, regex=r".*", checkpoint_interval_multiplier=200),
            settings=SubscriptionSettings(
                read_batch_size=50,
                live_buffer_size=100,
                history_buffer_size=100,
                max_retry_count=2,
                checkpoint_ms=100000,
            ),
        )

        info = await conn.subscriptions.get_info(group_name)
        assert info.group_name == group_name
        await conn.subscriptions.delete(group_name)
        with pytest.raises(grpc.aio._call.AioRpcError) as err:
            await conn.subscriptions.get_info(group_name)
        assert err.value.code() == grpc.StatusCode.NOT_FOUND


@pytest.mark.asyncio
async def test_list_subscription(client):
    group1 = str(uuid.uuid4())
    group2 = str(uuid.uuid4())
    stream = str(uuid.uuid4())
    settings = SubscriptionSettings(
        read_batch_size=9,
        live_buffer_size=10,
        history_buffer_size=10,
        max_subscriber_count=3,
        checkpoint_ms=5000,
    )
    async with client.connect() as conn:
        await conn.streams.append(stream, "evt_type", b"data")
        await conn.subscriptions.create_stream_subscription(
            group_name=group1,
            stream=stream,
            settings=settings,
        )
        await conn.subscriptions.create_all_subscription(
            group_name=group2,
            settings=settings,
        )

        subs = await conn.subscriptions.list()
        groups = [sub.group_name for sub in subs]
        assert group1 in groups
        assert group2 in groups

        [sub] = await conn.subscriptions.list(stream=stream)
        assert sub.group_name == group1
