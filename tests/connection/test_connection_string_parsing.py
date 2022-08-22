import pytest

from esdb.client import Configuration, Member, parse_connection_string


@pytest.mark.parametrize(
    "connection_string, config",
    (
        (
            "esdb://host1:2113,host2:2113?keepAliveTimeout=10000&keepAliveInterval=10000",
            Configuration(
                gossip_seed=[Member.Endpoint("host1", 2113), Member.Endpoint("host2", 2113)],
                dns_discover=False,
                keep_alive_timeout=10000,
                keep_alive_interval=10000,
            ),
        ),
        (
            "esdb+discover://host:2113",
            Configuration(dns_discover=True, address=Member.Endpoint(address="host", port=2113)),
        ),
    ),
)
def test_parse_connection_string(connection_string, config):
    assert parse_connection_string(connection_string) == config
