# esdb-py

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
  - [ ] filtering
  - [ ] exception handling
- [ ] subscriptions
- [ ] users
- [ ] tbd


# Setting things up
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

from client.client import ESClient

# For insecure connection without basic auth:
# client = ESClient("localhost:2113", tls=False)
with open("certs/ca/ca.crt", "rb") as fh:
  root_cert = fh.read()

client = ESClient("localhost:2111", root_certificates=root_cert, username="admin", password="changeit")

stream = f"test-{str(uuid.uuid4())}"

for i in range(10):
  append_result = client.streams.append(
    stream=stream,
    event_type="test_event",
    data={"i": i, "ts": datetime.datetime.utcnow().isoformat()},
  )

print("Forwards!")
for result in client.streams.read(stream=stream, count=10):
  print(result.data)

print("Backwards!")
for result in client.streams.read(stream=stream, count=10, backwards=True):
  print(result.data)

print("Forwards start from middle!")
for result in client.streams.read(stream=stream, count=10, revision=5):
  print(result.data)

print("Backwards start from middle!")
for result in client.streams.read(stream=stream, count=10, backwards=True, revision=5):
  print(result.data)
```

Async example:

```py
import asyncio
from client.client import AsyncESClient


async def append():
  client = AsyncESClient("localhost:2113")
  result = await client.streams.append("stream", "type", {"x": 1})
  assert result.commit_position > 0
  async for event in client.streams.read("stream", count=10):
    print(event)


asyncio.run(append())
```

Subscriptions:
```py
from client.client import ESClient

client = ESClient("localhost:2113", tls=False)
stream = "stream-name"
group = "group-name"

# emit some events to the same stream
for _ in range(10):
    client.streams.append(stream, "foobar", b"data")

# create a subscription
client.subscriptions.create_stream_subscription(stream=stream, group_name=group, revision=1)

# Read from subscription
# This will block and wait for messages
subscription = client.subscriptions.subscribe_to_stream(stream, group)
for event in subscription:
    # ... do work with the event ...
    # ack the event
    subscription.ack([event])
```