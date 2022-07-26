import pytest

from esclient import ESClient


@pytest.fixture
def client() -> ESClient:
    return ESClient("localhost:2113")
