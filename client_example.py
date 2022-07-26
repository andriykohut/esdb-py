import datetime

from esclient import ESClient

client = ESClient("localhost:2113")

append_result = client.streams.append(
    stream="test",
    event_type="order_placed",
    data={"x": 1, "y": 2, "ts": datetime.datetime.utcnow().isoformat()},
)
print("Forwards!")
for result in client.streams.read(stream="test", count=10):
    print(result.data)

print("Backwards!")
for result in client.streams.read(stream="test", count=10, backwards=True):
    print(result.data)
