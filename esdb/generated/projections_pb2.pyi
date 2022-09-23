"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.struct_pb2
import shared_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class CreateReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        class Transient(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            NAME_FIELD_NUMBER: builtins.int
            name: builtins.str
            def __init__(
                self,
                *,
                name: builtins.str = ...,
            ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal["name", b"name"]) -> None: ...

        class Continuous(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            NAME_FIELD_NUMBER: builtins.int
            EMIT_ENABLED_FIELD_NUMBER: builtins.int
            TRACK_EMITTED_STREAMS_FIELD_NUMBER: builtins.int
            name: builtins.str
            emit_enabled: builtins.bool
            track_emitted_streams: builtins.bool
            def __init__(
                self,
                *,
                name: builtins.str = ...,
                emit_enabled: builtins.bool = ...,
                track_emitted_streams: builtins.bool = ...,
            ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal["emit_enabled", b"emit_enabled", "name", b"name", "track_emitted_streams", b"track_emitted_streams"]) -> None: ...

        ONE_TIME_FIELD_NUMBER: builtins.int
        TRANSIENT_FIELD_NUMBER: builtins.int
        CONTINUOUS_FIELD_NUMBER: builtins.int
        QUERY_FIELD_NUMBER: builtins.int
        @property
        def one_time(self) -> shared_pb2.Empty: ...
        @property
        def transient(self) -> global___CreateReq.Options.Transient: ...
        @property
        def continuous(self) -> global___CreateReq.Options.Continuous: ...
        query: builtins.str
        def __init__(
            self,
            *,
            one_time: shared_pb2.Empty | None = ...,
            transient: global___CreateReq.Options.Transient | None = ...,
            continuous: global___CreateReq.Options.Continuous | None = ...,
            query: builtins.str = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["continuous", b"continuous", "mode", b"mode", "one_time", b"one_time", "transient", b"transient"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["continuous", b"continuous", "mode", b"mode", "one_time", b"one_time", "query", b"query", "transient", b"transient"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal["mode", b"mode"]) -> typing_extensions.Literal["one_time", "transient", "continuous"] | None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___CreateReq.Options: ...
    def __init__(
        self,
        *,
        options: global___CreateReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["options", b"options"]) -> None: ...

global___CreateReq = CreateReq

class CreateResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___CreateResp = CreateResp

class UpdateReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        QUERY_FIELD_NUMBER: builtins.int
        EMIT_ENABLED_FIELD_NUMBER: builtins.int
        NO_EMIT_OPTIONS_FIELD_NUMBER: builtins.int
        name: builtins.str
        query: builtins.str
        emit_enabled: builtins.bool
        @property
        def no_emit_options(self) -> shared_pb2.Empty: ...
        def __init__(
            self,
            *,
            name: builtins.str = ...,
            query: builtins.str = ...,
            emit_enabled: builtins.bool = ...,
            no_emit_options: shared_pb2.Empty | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["emit_enabled", b"emit_enabled", "emit_option", b"emit_option", "no_emit_options", b"no_emit_options"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["emit_enabled", b"emit_enabled", "emit_option", b"emit_option", "name", b"name", "no_emit_options", b"no_emit_options", "query", b"query"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal["emit_option", b"emit_option"]) -> typing_extensions.Literal["emit_enabled", "no_emit_options"] | None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___UpdateReq.Options: ...
    def __init__(
        self,
        *,
        options: global___UpdateReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["options", b"options"]) -> None: ...

global___UpdateReq = UpdateReq

class UpdateResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___UpdateResp = UpdateResp

class DeleteReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        DELETE_EMITTED_STREAMS_FIELD_NUMBER: builtins.int
        DELETE_STATE_STREAM_FIELD_NUMBER: builtins.int
        DELETE_CHECKPOINT_STREAM_FIELD_NUMBER: builtins.int
        name: builtins.str
        delete_emitted_streams: builtins.bool
        delete_state_stream: builtins.bool
        delete_checkpoint_stream: builtins.bool
        def __init__(
            self,
            *,
            name: builtins.str = ...,
            delete_emitted_streams: builtins.bool = ...,
            delete_state_stream: builtins.bool = ...,
            delete_checkpoint_stream: builtins.bool = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["delete_checkpoint_stream", b"delete_checkpoint_stream", "delete_emitted_streams", b"delete_emitted_streams", "delete_state_stream", b"delete_state_stream", "name", b"name"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___DeleteReq.Options: ...
    def __init__(
        self,
        *,
        options: global___DeleteReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["options", b"options"]) -> None: ...

global___DeleteReq = DeleteReq

class DeleteResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DeleteResp = DeleteResp

class StatisticsReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        ALL_FIELD_NUMBER: builtins.int
        TRANSIENT_FIELD_NUMBER: builtins.int
        CONTINUOUS_FIELD_NUMBER: builtins.int
        ONE_TIME_FIELD_NUMBER: builtins.int
        name: builtins.str
        @property
        def all(self) -> shared_pb2.Empty: ...
        @property
        def transient(self) -> shared_pb2.Empty: ...
        @property
        def continuous(self) -> shared_pb2.Empty: ...
        @property
        def one_time(self) -> shared_pb2.Empty: ...
        def __init__(
            self,
            *,
            name: builtins.str = ...,
            all: shared_pb2.Empty | None = ...,
            transient: shared_pb2.Empty | None = ...,
            continuous: shared_pb2.Empty | None = ...,
            one_time: shared_pb2.Empty | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["all", b"all", "continuous", b"continuous", "mode", b"mode", "name", b"name", "one_time", b"one_time", "transient", b"transient"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["all", b"all", "continuous", b"continuous", "mode", b"mode", "name", b"name", "one_time", b"one_time", "transient", b"transient"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal["mode", b"mode"]) -> typing_extensions.Literal["name", "all", "transient", "continuous", "one_time"] | None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___StatisticsReq.Options: ...
    def __init__(
        self,
        *,
        options: global___StatisticsReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["options", b"options"]) -> None: ...

global___StatisticsReq = StatisticsReq

class StatisticsResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Details(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        COREPROCESSINGTIME_FIELD_NUMBER: builtins.int
        VERSION_FIELD_NUMBER: builtins.int
        EPOCH_FIELD_NUMBER: builtins.int
        EFFECTIVENAME_FIELD_NUMBER: builtins.int
        WRITESINPROGRESS_FIELD_NUMBER: builtins.int
        READSINPROGRESS_FIELD_NUMBER: builtins.int
        PARTITIONSCACHED_FIELD_NUMBER: builtins.int
        STATUS_FIELD_NUMBER: builtins.int
        STATEREASON_FIELD_NUMBER: builtins.int
        NAME_FIELD_NUMBER: builtins.int
        MODE_FIELD_NUMBER: builtins.int
        POSITION_FIELD_NUMBER: builtins.int
        PROGRESS_FIELD_NUMBER: builtins.int
        LASTCHECKPOINT_FIELD_NUMBER: builtins.int
        EVENTSPROCESSEDAFTERRESTART_FIELD_NUMBER: builtins.int
        CHECKPOINTSTATUS_FIELD_NUMBER: builtins.int
        BUFFEREDEVENTS_FIELD_NUMBER: builtins.int
        WRITEPENDINGEVENTSBEFORECHECKPOINT_FIELD_NUMBER: builtins.int
        WRITEPENDINGEVENTSAFTERCHECKPOINT_FIELD_NUMBER: builtins.int
        coreProcessingTime: builtins.int
        version: builtins.int
        epoch: builtins.int
        effectiveName: builtins.str
        writesInProgress: builtins.int
        readsInProgress: builtins.int
        partitionsCached: builtins.int
        status: builtins.str
        stateReason: builtins.str
        name: builtins.str
        mode: builtins.str
        position: builtins.str
        progress: builtins.float
        lastCheckpoint: builtins.str
        eventsProcessedAfterRestart: builtins.int
        checkpointStatus: builtins.str
        bufferedEvents: builtins.int
        writePendingEventsBeforeCheckpoint: builtins.int
        writePendingEventsAfterCheckpoint: builtins.int
        def __init__(
            self,
            *,
            coreProcessingTime: builtins.int = ...,
            version: builtins.int = ...,
            epoch: builtins.int = ...,
            effectiveName: builtins.str = ...,
            writesInProgress: builtins.int = ...,
            readsInProgress: builtins.int = ...,
            partitionsCached: builtins.int = ...,
            status: builtins.str = ...,
            stateReason: builtins.str = ...,
            name: builtins.str = ...,
            mode: builtins.str = ...,
            position: builtins.str = ...,
            progress: builtins.float = ...,
            lastCheckpoint: builtins.str = ...,
            eventsProcessedAfterRestart: builtins.int = ...,
            checkpointStatus: builtins.str = ...,
            bufferedEvents: builtins.int = ...,
            writePendingEventsBeforeCheckpoint: builtins.int = ...,
            writePendingEventsAfterCheckpoint: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["bufferedEvents", b"bufferedEvents", "checkpointStatus", b"checkpointStatus", "coreProcessingTime", b"coreProcessingTime", "effectiveName", b"effectiveName", "epoch", b"epoch", "eventsProcessedAfterRestart", b"eventsProcessedAfterRestart", "lastCheckpoint", b"lastCheckpoint", "mode", b"mode", "name", b"name", "partitionsCached", b"partitionsCached", "position", b"position", "progress", b"progress", "readsInProgress", b"readsInProgress", "stateReason", b"stateReason", "status", b"status", "version", b"version", "writePendingEventsAfterCheckpoint", b"writePendingEventsAfterCheckpoint", "writePendingEventsBeforeCheckpoint", b"writePendingEventsBeforeCheckpoint", "writesInProgress", b"writesInProgress"]) -> None: ...

    DETAILS_FIELD_NUMBER: builtins.int
    @property
    def details(self) -> global___StatisticsResp.Details: ...
    def __init__(
        self,
        *,
        details: global___StatisticsResp.Details | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["details", b"details"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["details", b"details"]) -> None: ...

global___StatisticsResp = StatisticsResp

class StateReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        PARTITION_FIELD_NUMBER: builtins.int
        name: builtins.str
        partition: builtins.str
        def __init__(
            self,
            *,
            name: builtins.str = ...,
            partition: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "partition", b"partition"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___StateReq.Options: ...
    def __init__(
        self,
        *,
        options: global___StateReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["options", b"options"]) -> None: ...

global___StateReq = StateReq

class StateResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STATE_FIELD_NUMBER: builtins.int
    @property
    def state(self) -> google.protobuf.struct_pb2.Value: ...
    def __init__(
        self,
        *,
        state: google.protobuf.struct_pb2.Value | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["state", b"state"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["state", b"state"]) -> None: ...

global___StateResp = StateResp

class ResultReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        PARTITION_FIELD_NUMBER: builtins.int
        name: builtins.str
        partition: builtins.str
        def __init__(
            self,
            *,
            name: builtins.str = ...,
            partition: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "partition", b"partition"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___ResultReq.Options: ...
    def __init__(
        self,
        *,
        options: global___ResultReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["options", b"options"]) -> None: ...

global___ResultReq = ResultReq

class ResultResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESULT_FIELD_NUMBER: builtins.int
    @property
    def result(self) -> google.protobuf.struct_pb2.Value: ...
    def __init__(
        self,
        *,
        result: google.protobuf.struct_pb2.Value | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["result", b"result"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["result", b"result"]) -> None: ...

global___ResultResp = ResultResp

class ResetReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        WRITE_CHECKPOINT_FIELD_NUMBER: builtins.int
        name: builtins.str
        write_checkpoint: builtins.bool
        def __init__(
            self,
            *,
            name: builtins.str = ...,
            write_checkpoint: builtins.bool = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "write_checkpoint", b"write_checkpoint"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___ResetReq.Options: ...
    def __init__(
        self,
        *,
        options: global___ResetReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["options", b"options"]) -> None: ...

global___ResetReq = ResetReq

class ResetResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ResetResp = ResetResp

class EnableReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        name: builtins.str
        def __init__(
            self,
            *,
            name: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["name", b"name"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___EnableReq.Options: ...
    def __init__(
        self,
        *,
        options: global___EnableReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["options", b"options"]) -> None: ...

global___EnableReq = EnableReq

class EnableResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___EnableResp = EnableResp

class DisableReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        NAME_FIELD_NUMBER: builtins.int
        WRITE_CHECKPOINT_FIELD_NUMBER: builtins.int
        name: builtins.str
        write_checkpoint: builtins.bool
        def __init__(
            self,
            *,
            name: builtins.str = ...,
            write_checkpoint: builtins.bool = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "write_checkpoint", b"write_checkpoint"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___DisableReq.Options: ...
    def __init__(
        self,
        *,
        options: global___DisableReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["options", b"options"]) -> None: ...

global___DisableReq = DisableReq

class DisableResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DisableResp = DisableResp
