import pytest

from esdb.client import parse_connection_string


@pytest.mark.parametrize(
    "connection_string, config",
    (
        (
            "esdb://host1:2113,host2:2113,host3:2113?keepAliveTimeout=10000&keepAliveInterval=10000",
            {"dns_discover": False, "gossip_seed": [("host1", 2113), ("host2", 2113), ("host3", 2113)]},
        ),
        (
            "esdb+discover://host:2113?keepAliveTimeout=10000&keepAliveInterval=10000",
            {"dns_discover": True, "address": ("host", 2113)},
        ),
    ),
)
def test_parse_connection_string(connection_string, config):
    assert parse_connection_string(connection_string) == config
