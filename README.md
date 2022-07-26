# esdb-py

EventStoreDB Python gRPC client
> NOTE: This project is still work in progress

**Implemented parts**
- [ ] secure connection
- [ ] streams
  - [x] append
  - [x] batch append
  - [x] delete
  - [x] read
  - [x] tombstone
  - [ ] filtering
  - [ ] exception handling
  - [ ] async
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

from esclient import ESClient

client = ESClient("localhost:2113")

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
from esclient import AsyncESClient


async def append():
    client = AsyncESClient("localhost:2113")
    result = await client.streams.append("stream", "type", {"x": 1})
    assert result.commit_position > 0


asyncio.run(append())
```