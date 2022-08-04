from functools import lru_cache

import pytest

from esdb import ESClient


@lru_cache
def root_cert():
    with open("./certs/ca/ca.crt", "rb") as fh:
        return fh.read()


@pytest.fixture
def client() -> ESClient:
    return ESClient("localhost:2112", root_certificates=root_cert(), username="admin", password="changeit")
