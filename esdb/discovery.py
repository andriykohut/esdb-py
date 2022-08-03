import enum
import logging
import random
from typing import Optional

from esdb import gossip
from esdb.client import Connection

logger = logging.getLogger()

ALLOWED_STATES = (
  gossip.State.Follower,
  gossip.State.Leader,
  gossip.State.ReadOnlyReplica,
  gossip.State.PreReadOnlyReplica,
  gossip.State.ReadOnlyLeaderless,
)


class Preference(enum.Enum):
    RANDOM = enum.auto()
    LEADER = enum.auto()
    FOLLOWER = enum.auto()
    READ_ONLY_REPLICA = enum.auto()


def preference_to_states(pref: Preference) -> list[gossip.State]:
    if pref == Preference.RANDOM:
        return [random.choice(ALLOWED_STATES)]
    if pref == Preference.LEADER:
        return [gossip.State.Leader]
    if pref == Preference.FOLLOWER:
        return [gossip.State.Follower]
    if pref == Preference.READ_ONLY_REPLICA:
        return [gossip.State.ReadOnlyLeaderless, gossip.State.PreReadOnlyReplica, gossip.State.ReadOnlyReplica]


def find_best_member(members: list[gossip.Member], preference: Preference) -> Optional[gossip.Member]:
    allowed_members = [m for m in members if m.is_alive and m.endpoint is not None]
    random.shuffle(allowed_members)
    states = preference_to_states(preference)
    for member in allowed_members:
        if member.state in states:
            return member




async def discover(
    connection: Connection,
    endpoints: list[gossip.Member.Endpoint],
    interval: int = 100,
    max_attempts: int = 10,
    node_preference: Preference = Preference.LEADER,
) -> gossip.Member:
    for i in range(1, max_attempts + 1):
        endpoints_ = endpoints.copy()
        random.shuffle(endpoints_)
        for endpoint in endpoints_:
            members = await connection.gossip.get_members()
            if member := find_best_member(members, node_preference):
                return member.endpoint
