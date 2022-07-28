from __future__ import annotations

import json
from dataclasses import dataclass

from esdb.client.streams.base import ContentType
from esdb.generated.persistent_pb2 import ReadResp


@dataclass
class Event:
    id: str
    retry_count: int
    stream: str
    prepare_position: int
    commit_position: int
    metadata: dict
    type: str
    data: bytes | dict

    @staticmethod
    def from_read_response(response: ReadResp) -> Event:
        return Event(
            id=response.event.event.id.string,
            retry_count=response.event.retry_count,
            stream=response.event.event.stream_identifier.stream_name.decode(),
            prepare_position=response.event.event.prepare_position,
            commit_position=response.event.event.commit_position,
            metadata=response.event.event.metadata,
            type=response.event.event.metadata["type"],
            data=json.loads(response.event.event.data)
            if response.event.event.metadata["content-type"] == ContentType.JSON
            else response.event.event.data,
        )
