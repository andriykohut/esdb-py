"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import shared_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class ClusterInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MEMBERS_FIELD_NUMBER: builtins.int
    @property
    def members(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___MemberInfo]: ...
    def __init__(
        self,
        *,
        members: collections.abc.Iterable[global___MemberInfo] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["members", b"members"]) -> None: ...

global___ClusterInfo = ClusterInfo

@typing_extensions.final
class EndPoint(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ADDRESS_FIELD_NUMBER: builtins.int
    PORT_FIELD_NUMBER: builtins.int
    address: builtins.str
    port: builtins.int
    def __init__(
        self,
        *,
        address: builtins.str = ...,
        port: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["address", b"address", "port", b"port"]) -> None: ...

global___EndPoint = EndPoint

@typing_extensions.final
class MemberInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _VNodeState:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _VNodeStateEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[MemberInfo._VNodeState.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        Initializing: MemberInfo._VNodeState.ValueType  # 0
        DiscoverLeader: MemberInfo._VNodeState.ValueType  # 1
        Unknown: MemberInfo._VNodeState.ValueType  # 2
        PreReplica: MemberInfo._VNodeState.ValueType  # 3
        CatchingUp: MemberInfo._VNodeState.ValueType  # 4
        Clone: MemberInfo._VNodeState.ValueType  # 5
        Follower: MemberInfo._VNodeState.ValueType  # 6
        PreLeader: MemberInfo._VNodeState.ValueType  # 7
        Leader: MemberInfo._VNodeState.ValueType  # 8
        Manager: MemberInfo._VNodeState.ValueType  # 9
        ShuttingDown: MemberInfo._VNodeState.ValueType  # 10
        Shutdown: MemberInfo._VNodeState.ValueType  # 11
        ReadOnlyLeaderless: MemberInfo._VNodeState.ValueType  # 12
        PreReadOnlyReplica: MemberInfo._VNodeState.ValueType  # 13
        ReadOnlyReplica: MemberInfo._VNodeState.ValueType  # 14
        ResigningLeader: MemberInfo._VNodeState.ValueType  # 15

    class VNodeState(_VNodeState, metaclass=_VNodeStateEnumTypeWrapper): ...
    Initializing: MemberInfo.VNodeState.ValueType  # 0
    DiscoverLeader: MemberInfo.VNodeState.ValueType  # 1
    Unknown: MemberInfo.VNodeState.ValueType  # 2
    PreReplica: MemberInfo.VNodeState.ValueType  # 3
    CatchingUp: MemberInfo.VNodeState.ValueType  # 4
    Clone: MemberInfo.VNodeState.ValueType  # 5
    Follower: MemberInfo.VNodeState.ValueType  # 6
    PreLeader: MemberInfo.VNodeState.ValueType  # 7
    Leader: MemberInfo.VNodeState.ValueType  # 8
    Manager: MemberInfo.VNodeState.ValueType  # 9
    ShuttingDown: MemberInfo.VNodeState.ValueType  # 10
    Shutdown: MemberInfo.VNodeState.ValueType  # 11
    ReadOnlyLeaderless: MemberInfo.VNodeState.ValueType  # 12
    PreReadOnlyReplica: MemberInfo.VNodeState.ValueType  # 13
    ReadOnlyReplica: MemberInfo.VNodeState.ValueType  # 14
    ResigningLeader: MemberInfo.VNodeState.ValueType  # 15

    INSTANCE_ID_FIELD_NUMBER: builtins.int
    TIME_STAMP_FIELD_NUMBER: builtins.int
    STATE_FIELD_NUMBER: builtins.int
    IS_ALIVE_FIELD_NUMBER: builtins.int
    HTTP_END_POINT_FIELD_NUMBER: builtins.int
    @property
    def instance_id(self) -> shared_pb2.UUID: ...
    time_stamp: builtins.int
    state: global___MemberInfo.VNodeState.ValueType
    is_alive: builtins.bool
    @property
    def http_end_point(self) -> global___EndPoint: ...
    def __init__(
        self,
        *,
        instance_id: shared_pb2.UUID | None = ...,
        time_stamp: builtins.int = ...,
        state: global___MemberInfo.VNodeState.ValueType = ...,
        is_alive: builtins.bool = ...,
        http_end_point: global___EndPoint | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["http_end_point", b"http_end_point", "instance_id", b"instance_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["http_end_point", b"http_end_point", "instance_id", b"instance_id", "is_alive", b"is_alive", "state", b"state", "time_stamp", b"time_stamp"]) -> None: ...

global___MemberInfo = MemberInfo
