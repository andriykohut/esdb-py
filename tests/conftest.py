import asyncio
from functools import lru_cache

import grpc
import pytest

from esdb import ESClient
from esdb.client import Connection
from esdb.exceptions import StreamNotFound


@lru_cache
def root_cert():
    with open("./certs/ca/ca.crt", "rb") as fh:
        return fh.read()


@pytest.fixture
def client() -> ESClient:
    return ESClient(
        "localhost:2111",
        root_certificates=root_cert(),
        username="admin",
        password="changeit",
        discover=True,
    )


@pytest.fixture
def wait_for_stream():
    async def _wait_for_steam(c: Connection, stream: str, attempts: int = 10, delay: int = 0.1) -> None:
        for _ in range(attempts):
            try:
                async for _ in c.streams.read(stream=stream, count=1):
                    return
            except StreamNotFound:
                await asyncio.sleep(delay)

    return _wait_for_steam
