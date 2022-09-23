import pytest

from esdb import ESClient


@pytest.fixture
def client() -> ESClient:
    return ESClient("esdb+discover://admin:changeit@localhost:2111?tlscafile=certs/ca/ca.crt")
