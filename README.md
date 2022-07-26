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
6. Try running the example `python client_example.py`