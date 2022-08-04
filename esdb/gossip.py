from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass
from typing import Optional

from esdb.generated.gossip_pb2 import ClusterInfo, MemberInfo
from esdb.generated.gossip_pb2_grpc import GossipStub
from esdb.generated.shared_pb2 import Empty


class State(enum.IntEnum):
    Initializing = 0
    DiscoverLeader = enum.auto()
    Unknown = enum.auto()
    PreReplica = enum.auto()
    CatchingUp = enum.auto()
    Clone = enum.auto()
    Follower = enum.auto()
    PreLeader = enum.auto()
    Leader = enum.auto()
    Manager = enum.auto()
    ShuttingDown = enum.auto()
    Shutdown = enum.auto()
    ReadOnlyLeaderless = enum.auto()
    PreReadOnlyReplica = enum.auto()
    ReadOnlyReplica = enum.auto()
    ResigningLeader = enum.auto()


@dataclass
class Member:
    @dataclass
    class Endpoint:
        address: str
        port: int

    timestamp: datetime.datetime
    state: State
    is_alive: bool
    endpoint: Optional[Endpoint]

    @classmethod
    def from_protobuf(cls, m: MemberInfo) -> Member:
        return cls(
            timestamp=datetime.datetime.fromtimestamp(m.time_stamp / 10000000, datetime.timezone.utc),
            state=State(m.state),
            is_alive=m.is_alive,
            endpoint=cls.Endpoint(m.http_end_point.address, m.http_end_point.port)
            if m.http_end_point.address
            else None,
        )


class Gossip:
    def __init__(self, stub: GossipStub) -> None:
        self._stub = stub

    async def get_members(self) -> list[Member]:
        info: ClusterInfo = await self._stub.Read(Empty())
        return [Member.from_protobuf(m) for m in info.members]
