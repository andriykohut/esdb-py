# esdb-py

[![PyPI version](https://badge.fury.io/py/esdb.svg)](https://pypi.org/project/esdb/)

**EventStoreDB Python gRPC client**
> NOTE: This project is still work in progress

<!-- TOC -->
* [Completed features](#completed-features)
* [Installation](#installation)
* [Development](#development)
* [Usage](#usage)
  * [Append/Read](#appendread)
  * [Batch append](#batch-append)
  * [Transient subscription to all events with filtering](#transient-subscription-to-all-events-with-filtering)
  * [Persistent subscriptions](#persistent-subscriptions)
<!-- TOC -->

## Completed features
- [x] secure connection
- [x] basic auth
- [x] streams
  - [x] append
  - [x] batch append
  - [x] delete
  - [x] read stream
  - [x] read all with stream/event type filters
  - [x] transient subscriptions
  - [x] tombstone
  - [x] filtering
- [x] persistent subscriptions
    - [x] create
    - [x] read
    - [ ] update
    - [ ] delete
    - [ ] list
    - [ ] info
    - [ ] reply parked events 
- [ ] CRUD for projections
- [ ] users
- [ ] other connection options
  - [ ] multi-node gossip

## Installation
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

# Usage

Have a look at [tests](https://github.com/andriykohut/esdb-py/tree/main/tests) for more examples.

## Append/Read

```py
import asyncio
import datetime
import uuid

from esdb.client import ESClient

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


async def streams():
  async with client.connect() as conn:
    for i in range(10):
      append_result = await conn.streams.append(
        stream=stream,
        event_type="test_event",
        data={"i": i, "ts": datetime.datetime.utcnow().isoformat()},
      )

    print("Forwards!")
    async for result in conn.streams.read(stream=stream, count=10):
      print(result.data)

    print("Backwards!")
    async for result in conn.streams.read(stream=stream, count=10, backwards=True):
      print(result.data)

    print("Forwards start from middle!")
    async for result in conn.streams.read(stream=stream, count=10, revision=5):
      print(result.data)

    print("Backwards start from middle!")
    async for result in conn.streams.read(stream=stream, count=10, backwards=True, revision=5):
      print(result.data)

    # Create a transient subscription to a stream
    async for result in conn.streams.read(stream=stream, subscribe=True):
      print(result.data)


asyncio.run(streams())
```

## Batch append
```py
import asyncio
import uuid

from esdb.client import ESClient
from esdb.client.streams import Message


async def batch_append():
    stream = str(uuid.uuid4())
    messages: list[Message] = [
        Message(event_type="one", data={"item": 1}),
        Message(event_type="one", data={"item": 2}),
        Message(event_type="one", data={"item": 3}),
        Message(event_type="two", data={"item": 1}),
        Message(event_type="two", data={"item": 2}),
        Message(event_type="two", data={"item": 3}),
    ]
    async with ESClient("localhost:2113", tls=False).connect() as conn:
        response = await conn.streams.batch_append(stream=stream, messages=messages)
        assert response.current_revision == 5
        events = [e async for e in conn.streams.read(stream=stream, count=50)]
        assert len(events) == 6


asyncio.run(batch_append())
```

## Transient subscription to all events with filtering

```py
import uuid
import asyncio

from esdb.client import ESClient
from esdb.client.streams import Filter


async def filters():
  async with ESClient("localhost:2113", tls=False).connect() as conn:
    for i in range(10):
        await conn.streams.append(stream=str(uuid.uuid4()), event_type=f"prefix-{i}", data=b"")
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

## Persistent subscriptions

```python
import asyncio
from esdb.client import ESClient
from esdb.client.subscriptions import SubscriptionSettings, NackAction

client = ESClient("localhost:2113", tls=False)

stream = "stream-foo"
group = "group-bar"


async def persistent():
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
      try:
        # do work with event
        print(event)
        await subscription.ack([event])
      except Exception as err:
        await subscription([event], NackAction.RETRY, reason=str(err))


asyncio.run(persistent())
```