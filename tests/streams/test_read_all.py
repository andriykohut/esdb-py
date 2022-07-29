import uuid

from esdb.client.streams.base import Filter


def test_read_all_filter_by_event_type(client):
    event_type = str(uuid.uuid4())
    with client.connect() as conn:
        for _ in range(20):
            conn.streams.append(
                stream=str(uuid.uuid4()),
                event_type=event_type,
                data=b"",
            )

        assert (
            len(
                list(
                    conn.streams.read_all(
                        count=500,
                        filter_by=Filter(
                            kind=Filter.Kind.EVENT_TYPE,
                            regex=event_type,
                        ),
                    )
                )
            )
            == 20
        )


def test_read_all_filter_by_stream_name(client):
    stream_prefix = str(uuid.uuid4())
    with client.connect() as conn:
        for i in range(20):
            conn.streams.append(
                stream=f"{stream_prefix}-{i}",
                event_type="i-dont-care",
                data=b"",
            )

        assert (
            len(
                list(
                    conn.streams.read_all(
                        count=500,
                        filter_by=Filter(
                            kind=Filter.Kind.STREAM,
                            regex=stream_prefix,
                        ),
                    )
                )
            )
            == 20
        )
