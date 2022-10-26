# esdb-py

[![PyPI version](https://badge.fury.io/py/esdb.svg)](https://pypi.org/project/esdb/)
[![codecov](https://codecov.io/gh/andriykohut/esdb-py/branch/main/graph/badge.svg?token=YVDPTDBPFB)](https://codecov.io/gh/andriykohut/esdb-py)

## EventStoreDB Python gRPC client

> NOTE: This project is still work in progress

<!-- TOC -->
* [Completed features](#completed-features)
* [Installation](#installation)
* [Development](#development)
* [Usage](#usage)
  * [Connection string](#connection-string)
  * [Discovery and node preferences](#discovery-and-node-preferences)
  * [Connection configuration](#connection-configuration)
  * [Append, Read, Catch-up subscriptions](#append-read-catch-up-subscriptions)
  * [Batch append](#batch-append)
  * [Catch-up subscription to all events with filtering](#catch-up-subscription-to-all-events-with-filtering)
  * [Persistent subscriptions](#persistent-subscriptions)
<!-- TOC -->

## Completed features

* [x] secure connection
* [x] basic auth
* [x] connection string parsing
* [x] streams
  * [x] append
  * [x] batch append (v21.10+)
  * [x] delete
  * [x] read stream
  * [x] read all with stream/event type filters (v21.10+)
  * [x] catch-up subscriptions
  * [x] tombstone
  * [x] filtering
* [x] persistent subscriptions
  * [x] create
  * [x] read stream
  * [x] read all with filter (v21.10+)
  * [x] update
  * [x] delete
  * [x] list
  * [x] info
  * [ ] reply parked events
* [ ] CRUD for projections
* [ ] users

## Installation

Using pip:

```sh
pip install esdb
```

Using poetry:

```sh
poetry add esdb
```

## Development

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Create virtualenv (i.e. using pyenv):

    ```sh
    pyenv install 3.11.0
    pyenv virtualenv 3.11.0 esdb-py
    pyenv local esdb-py
    ```

3. Install deps with `poetry install`
4. Start eventstore in docker: `make run-esdb`
5. Run the tests: `pytest tests`

## Usage

Have a look at [tests](https://github.com/andriykohut/esdb-py/tree/main/tests) for more examples.

### Connection string examples

DNS discovery with credentials, discovery configuration, node preference and ca file path
```
esdb+discover://admin:changeit@localhost:2111?discoveryInterval=0&maxDiscoverAttempts=3&tlsCafile=certs/ca/ca.crt&nodePreference=follower
```

Single-node insecure connection
```
esdb://localhost:2111?tls=false
```

Supported parameters:
 - `discoveryInterval`
 - `gossipTimeout`
 - `maxDiscoverAttempts`
 - `nodePreference`
 - `keepAliveInterval`
 - `keepAliveTimeout`
 - `tls`
 - `tlsCafile`
 - `tlsVerifyCert`
 - `defaultDeadline`


Connection string can be generated [here](https://developers.eventstore.com/clients/grpc/#connection-details).

### Discovery and node preferences

```py
from esdb import ESClient

client = ESClient("esdb+discover://admin:changeit@localhost:2111?nodePreference=follower")

```

### Connection configuration

```py
from esdb import ESClient

# Connect without TLS
client = ESClient("esdb://localhost:2111?tls=false")

# Secure connection with basic auth and keepalive
client = ESClient("esdb://admin:changeit@localhost:2111?tlsCafile=certs/ca/ca.crt&keepAliveInterval=5&keepAliveTimeout=5")
```

### Append, Read, Catch-up subscriptions

```py
import asyncio
import datetime
import uuid

from esdb import ESClient


client = ESClient("esdb+discover://admin:changeit@localhost:2111")
stream = f"test-{str(uuid.uuid4())}"


async def streams():
    async with client.connect() as conn:
        # Appending to stream
        for i in range(10):
            append_result = await conn.streams.append(
                stream=stream,
                event_type="test_event",
                data={"i": i, "ts": datetime.datetime.utcnow().isoformat()},
            )

        # Read up to 10 events
        async for result in conn.streams.read(stream=stream, count=10):
            print(result.data)

        # Read up to 10 events, backwards
        async for result in conn.streams.read(stream=stream, count=10, backwards=True):
            print(result.data)

        # Read up to 10 events, starting from 5th event
        async for result in conn.streams.read(stream=stream, count=10, revision=5):
            print(result.data)

        # Read up to 10 events backwards, starting from 5th event
        async for result in conn.streams.read(stream=stream, count=10, backwards=True, revision=5):
            print(result.data)

        # Create a catch-up subscription to a stream
        async for result in conn.streams.read(stream=stream, subscribe=True):
            print(result.data)


asyncio.run(streams())
```

### Batch append

```py
import asyncio
import uuid

from esdb import ESClient
from esdb.streams import Message


async def batch_append():
    # Append multiple events in as a single batch
    # Batch append is not supported on EventStore < v21.10
    stream = str(uuid.uuid4())
    messages: list[Message] = [
        Message(event_type="one", data={"item": 1}),
        Message(event_type="one", data={"item": 2}),
        Message(event_type="one", data={"item": 3}),
        Message(event_type="two", data={"item": 1}),
        Message(event_type="two", data={"item": 2}),
        Message(event_type="two", data={"item": 3}),
    ]
    async with ESClient("esdb+discover://admin:changeit@localhost:2111").connect() as conn:
        response = await conn.streams.batch_append(stream=stream, messages=messages)
        assert response.current_revision == 5
        events = [e async for e in conn.streams.read(stream=stream, count=50)]
        assert len(events) == 6


asyncio.run(batch_append())
```

### Catch-up subscription to all events with filtering

```py
import uuid
import asyncio

from esdb import ESClient
from esdb.shared import Filter


async def filters():
    async with ESClient("esdb+discover://admin:changeit@localhost:2111").connect() as conn:
        # Append 10 events with the same prefix to random streams
        for i in range(10):
            await conn.streams.append(stream=str(uuid.uuid4()), event_type=f"prefix-{i}", data=b"")
        # subscribe to events from all streams, filtering by event type
        async for event in conn.streams.read_all(
                subscribe=True,  # subscribe will wait for events, use count=<n> to read <n> events and stop
                filter_by=Filter(
                    kind=Filter.Kind.EVENT_TYPE,
                    regex="^prefix-",
                    # Checkpoint only required when subscribe=True, it's not needed when using count=<int>
                    checkpoint_interval_multiplier=1000,
                ),
        ):
            print(event)


asyncio.run(filters())
```

### Persistent subscriptions

```python
import asyncio
from esdb import ESClient
from esdb.shared import Filter
from esdb.subscriptions import SubscriptionSettings, NackAction

client = ESClient("esdb+discover://admin:changeit@localhost:2111")

stream = "stream-foo"
group = "group-bar"


async def persistent():
    async with client.connect() as conn:
        # emit some events to the same stream
        for i in range(50):
            await conn.streams.append(stream, "foobar", {"i": i})

        # create a stream subscription
        await conn.subscriptions.create_stream_subscription(
            stream=stream,
            group_name=group,
            settings=SubscriptionSettings(
                max_subscriber_count=50,
                read_batch_size=5,
                live_buffer_size=10,
                history_buffer_size=10,
                consumer_strategy=SubscriptionSettings.ConsumerStrategy.ROUND_ROBIN,
                checkpoint_ms=10000,
            ),
        )

        # create subscription to all events with filtering
        # Only supported on EventStore v21.10+
        await conn.subscriptions.create_all_subscription(
            group_name="subscription_group",
            filter_by=Filter(kind=Filter.Kind.EVENT_TYPE, regex="^some_type$", checkpoint_interval_multiplier=200),
            settings=SubscriptionSettings(
                read_batch_size=50,
                live_buffer_size=100,
                history_buffer_size=100,
                max_retry_count=2,
                checkpoint_ms=20000,
            ),
        )

    # read from a subscription
    async with client.connect() as conn:
        sub = conn.subscriptions.subscribe(stream=stream, group_name=group, buffer_size=5)
        async for event in sub:
            try:
                # do work with event
                print(event)
                await sub.ack([event])
            except Exception as err:
                await sub.nack([event], NackAction.RETRY, reason=str(err))

        # get subscription info
        info = await conn.subscriptions.get_info(group, stream)
        assert info.group_name == group

        # delete subscription
        await conn.subscriptions.delete(group, stream)
        
        # list subscriptions
        subs = await conn.subscriptions.list()
        for sub in subs:
            print(sub.total_items)


asyncio.run(persistent())
```
