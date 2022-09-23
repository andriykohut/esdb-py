import enum
from dataclasses import dataclass
from typing import Optional, Type, TypeVar

from esdb.generated.persistent_pb2 import CreateReq
from esdb.generated.shared_pb2 import Empty
from esdb.generated.streams_pb2 import ReadReq

MessageType = TypeVar("MessageType", ReadReq.Options.FilterOptions, CreateReq.AllOptions.FilterOptions)


@dataclass
class Filter:
    class Kind(enum.Enum):
        STREAM = "stream"
        EVENT_TYPE = "event_type"

    kind: Kind
    regex: str
    prefixes: Optional[list[str]] = None
    checkpoint_interval_multiplier: Optional[int] = None

    def to_protobuf(self, message_type: Type[MessageType]) -> MessageType:
        expression_type = message_type.Expression
        stream_identifier = None
        event_type = None
        if self.kind == self.Kind.STREAM:
            stream_identifier = expression_type(regex=self.regex, prefix=self.prefixes)
        elif self.kind == self.Kind.EVENT_TYPE:
            event_type = expression_type(regex=self.regex, prefix=self.prefixes)
        options = message_type(
            stream_identifier=stream_identifier,
            event_type=event_type,
            max=0,  # TODO: This apparently does nothing ¯\_(ツ)_/¯
            count=Empty(),
        )
        if self.checkpoint_interval_multiplier:
            options.checkpointIntervalMultiplier = self.checkpoint_interval_multiplier
        return options
