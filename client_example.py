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
