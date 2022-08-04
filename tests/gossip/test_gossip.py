import pytest

from esdb.gossip import State


@pytest.mark.asyncio
async def test_gossip(client):
    async with client.connect() as conn:
        members = await conn.gossip.get_members()
        assert len([m for m in members if m.state == State.Leader]) == 1
        assert len([m for m in members if m.state == State.Follower]) == 2
