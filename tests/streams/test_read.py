import uuid
from unittest.mock import ANY

import pytest

from streams import ReadResult


@pytest.mark.parametrize(
    ["data", "expected_content_type"],
    (
        (b"some bytes", "application/octet-stream"),
        ({"foo": "bar"}, "application/json"),
    ),
)
def test_append_and_read(data, client, expected_content_type):
    stream = str(uuid.uuid4())
    client.streams.append(stream=stream, event_type="foobar", data=data, custom_metadata={"raisedBy": "me"})
    [response] = client.streams.read(stream=stream, count=1)

    assert isinstance(response, ReadResult)
    assert response.data == data
    assert response.commit_position == 0
    assert response.prepare_position == 0
    assert isinstance(response.id, str)
    assert response.metadata == {"created": ANY, "content-type": expected_content_type, "type": "foobar"}
    assert response.stream_name == stream
    assert response.custom_metadata == {"raisedBy": "me"}
