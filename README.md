# esdb-py

EventStoreDB Python gRPC client
> NOTE: This project is still work in progress


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
5. Try running the example `python client_example.py`
```py
    channel = grpc.insecure_channel("localhost:2113")
    stub = StreamsStub(channel)
    streams = Streams(stub)
    result = streams.append(
        stream="test",
        event_type="order_placed",
        data={"x": 1, "y": 2, "ts": datetime.datetime.utcnow().isoformat()},
    )
    print("Forwards!")
    for result in streams.read(stream="test", count=10):
        print(result.data)

    print("Backwards!")
    for result in streams.read(stream="test", count=10, backwards=True):
        print(result.data)
```