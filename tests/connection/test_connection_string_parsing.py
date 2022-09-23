import pytest

from esdb.client import Configuration, Member, Preference, parse_connection_string


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
        (
            "esdb://user:pass@host:2113?tls=False",
            Configuration(
                dns_discover=False,
                address=Member.Endpoint(address="host", port=2113),
                username="user",
                password="pass",
                disable_tls=True,
            ),
        ),
        (
            "esdb://host:2113?nodePreference=follower&tlsVerifyCert=false&defaultDeadline=21&gossipTimeout=12",
            Configuration(
                dns_discover=False,
                address=Member.Endpoint(address="host", port=2113),
                node_preference=Preference.FOLLOWER,
                verify_cert=False,
                default_deadline=21,
                gossip_timeout=12,
            ),
        ),
        (
            "esdb://host",
            Configuration(
                dns_discover=False,
                address=Member.Endpoint(address="host", port=2113),
            ),
        ),
    ),
)
def test_parse_connection_string(connection_string, config):
    assert parse_connection_string(connection_string) == config


@pytest.mark.parametrize(
    "connection_string, error_msg",
    (
        ("foo://host:2113", "esdb:// or esdb+discover:// scheme is required"),
        ("esdb://ho:st:2113", "Too many colons in a host"),
        ("esdb://host:foo", "foo port is not a number"),
        ("esdb://host?tls=true&tls=false", "Too many values for tls"),
        ("esdb://host?foo=1", "Invalid option foo"),
        ("esdb://user@host?foo=1", "Invalid user credentials"),
        ("esdb://user:@host?foo=1", "Password is required"),
        ("esdb://:password@host?foo=1", "Username is required"),
    ),
)
def test_invalid_string(connection_string, error_msg):
    with pytest.raises(ValueError) as err:
        parse_connection_string(connection_string)

    assert str(err.value) == error_msg
