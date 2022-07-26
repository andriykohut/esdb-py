import pytest

from esclient import ESClient, AsyncESClient


@pytest.fixture
def client() -> ESClient:
    return ESClient("localhost:2113")


@pytest.fixture
def async_client() -> AsyncESClient:
    return AsyncESClient("localhost:2113")