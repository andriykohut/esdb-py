# esdb-py

[![PyPI version](https://badge.fury.io/py/esdb.svg)](https://pypi.org/project/esdb/)

EventStoreDB Python gRPC client
> NOTE: This project is still work in progress

**Implemented parts**
- [x] secure connection
- [x] basic auth
- [ ] other connection options
  - [ ] multi-node gossip
  - [ ] keepalive
- [x] async client
- [ ] streams
  - [x] append
  - [x] batch append
  - [x] delete
  - [x] read
  - [x] tombstone
  - [x] filtering
  - [ ] exception handling
- [x] subscriptions
- [ ] users

# Installation
Using pip:
```sh
pip install esdb
```
Using poetry:
```sh
poetry add esdb
```

# Development
1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Create virtualenv (i.e. using pyenv):
```sh
pyenv install 3.10.5
pyenv virtualenv 3.10.5 esdb-py
pyenv local esdb-py
```
3. Install deps with `poetry install`
4. Start eventstore in docker: `make run-esdb`
5. Run the tests: `pytest tests`

Usage:

```py
import datetime
import uuid

from esdb.client.client import ESClient

# For insecure connection without basic auth:
# client = ESClient("localhost:2113", tls=False)
with open("certs/ca/ca.crt", "rb") as fh:
  root_cert = fh.read()

client = ESClient(
    "localhost:2111",
    root_certificates=root_cert,
    username="admin",
    password="changeit",
    keepalive_time_ms=5000,
    keepalive_timeout_ms=10000,
)

stream = f"test-{str(uuid.uuid4())}"

with client.connect() as conn:
    for i in range(10):
        append_result = conn.streams.append(
            stream=stream,
            event_type="test_event",
            data={"i": i, "ts": datetime.datetime.utcnow().isoformat()},
        )

    print("Forwards!")
    for result in conn.streams.read(stream=stream, count=10):
        print(result.data)

    print("Backwards!")
    for result in conn.streams.read(stream=stream, count=10, backwards=True):
        print(result.data)

    print("Forwards start from middle!")
    for result in conn.streams.read(stream=stream, count=10, revision=5):
        print(result.data)

    print("Backwards start from middle!")
    for result in conn.streams.read(stream=stream, count=10, backwards=True, revision=5):
        print(result.data)
```

Async example:

```py
import asyncio

from esdb.client.client import AsyncESClient


async def append():
    client = AsyncESClient("localhost:2113", tls=False)
    async with client.connect() as conn:
        result = await conn.streams.append("stream", "type", {"x": 1})
        assert result.commit_position > 0
        async for event in conn.streams.read("stream", count=10):
            print(event)


asyncio.run(append())
```

Subscriptions:
```py
from esdb.client.client import ESClient
from esdb.client.subscriptions.base import SubscriptionSettings, NackAction

client = ESClient("localhost:2113", tls=False)
stream = "stream-name"
group = "group-name"

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

    # Read from subscription
    # This will block and wait for messages
    subscription = conn.subscriptions.subscribe_to_stream(stream, group, buffer_size=10)
    for event in subscription:
        try:
            # ... do work with the event ...
            # ack the event
            subscription.ack([event])
        except Exception as err:
            subscription.nack([event], NackAction.RETRY, reason=str(err))
          
        
```

Async subscriptions
```python
from esdb.client.client import AsyncESClient
from esdb.client.subscriptions.base import SubscriptionSettings

client = AsyncESClient("localhost:2113", tls=False)

stream = "stream-foo"
group = "group-bar"

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

async with client.connect() as conn:
    subscription = conn.subscriptions.subscribe_to_stream(stream=stream, group_name=group, buffer_size=5)
    async for event in subscription:
        await subscription.ack([event])
```