import pytest


@pytest.mark.asyncio
async def test_gossip(client):
    async with client.connect() as conn:
        members = await conn.gossip.get_members()
        print(members[0])
