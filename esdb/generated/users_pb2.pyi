"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class CreateReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        LOGIN_NAME_FIELD_NUMBER: builtins.int
        PASSWORD_FIELD_NUMBER: builtins.int
        FULL_NAME_FIELD_NUMBER: builtins.int
        GROUPS_FIELD_NUMBER: builtins.int
        login_name: builtins.str
        password: builtins.str
        full_name: builtins.str
        @property
        def groups(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
        def __init__(
            self,
            *,
            login_name: builtins.str = ...,
            password: builtins.str = ...,
            full_name: builtins.str = ...,
            groups: collections.abc.Iterable[builtins.str] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["full_name", b"full_name", "groups", b"groups", "login_name", b"login_name", "password", b"password"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___CreateReq.Options: ...
    def __init__(
        self,
        *,
        options: global___CreateReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["options", b"options"]) -> None: ...

global___CreateReq = CreateReq

@typing.final
class CreateResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___CreateResp = CreateResp

@typing.final
class UpdateReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        LOGIN_NAME_FIELD_NUMBER: builtins.int
        PASSWORD_FIELD_NUMBER: builtins.int
        FULL_NAME_FIELD_NUMBER: builtins.int
        GROUPS_FIELD_NUMBER: builtins.int
        login_name: builtins.str
        password: builtins.str
        full_name: builtins.str
        @property
        def groups(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
        def __init__(
            self,
            *,
            login_name: builtins.str = ...,
            password: builtins.str = ...,
            full_name: builtins.str = ...,
            groups: collections.abc.Iterable[builtins.str] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["full_name", b"full_name", "groups", b"groups", "login_name", b"login_name", "password", b"password"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___UpdateReq.Options: ...
    def __init__(
        self,
        *,
        options: global___UpdateReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["options", b"options"]) -> None: ...

global___UpdateReq = UpdateReq

@typing.final
class UpdateResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___UpdateResp = UpdateResp

@typing.final
class DeleteReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        LOGIN_NAME_FIELD_NUMBER: builtins.int
        login_name: builtins.str
        def __init__(
            self,
            *,
            login_name: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["login_name", b"login_name"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___DeleteReq.Options: ...
    def __init__(
        self,
        *,
        options: global___DeleteReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["options", b"options"]) -> None: ...

global___DeleteReq = DeleteReq

@typing.final
class DeleteResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DeleteResp = DeleteResp

@typing.final
class EnableReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        LOGIN_NAME_FIELD_NUMBER: builtins.int
        login_name: builtins.str
        def __init__(
            self,
            *,
            login_name: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["login_name", b"login_name"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___EnableReq.Options: ...
    def __init__(
        self,
        *,
        options: global___EnableReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["options", b"options"]) -> None: ...

global___EnableReq = EnableReq

@typing.final
class EnableResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___EnableResp = EnableResp

@typing.final
class DisableReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        LOGIN_NAME_FIELD_NUMBER: builtins.int
        login_name: builtins.str
        def __init__(
            self,
            *,
            login_name: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["login_name", b"login_name"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___DisableReq.Options: ...
    def __init__(
        self,
        *,
        options: global___DisableReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["options", b"options"]) -> None: ...

global___DisableReq = DisableReq

@typing.final
class DisableResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DisableResp = DisableResp

@typing.final
class DetailsReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        LOGIN_NAME_FIELD_NUMBER: builtins.int
        login_name: builtins.str
        def __init__(
            self,
            *,
            login_name: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["login_name", b"login_name"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___DetailsReq.Options: ...
    def __init__(
        self,
        *,
        options: global___DetailsReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["options", b"options"]) -> None: ...

global___DetailsReq = DetailsReq

@typing.final
class DetailsResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class UserDetails(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        @typing.final
        class DateTime(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            TICKS_SINCE_EPOCH_FIELD_NUMBER: builtins.int
            ticks_since_epoch: builtins.int
            def __init__(
                self,
                *,
                ticks_since_epoch: builtins.int = ...,
            ) -> None: ...
            def ClearField(self, field_name: typing.Literal["ticks_since_epoch", b"ticks_since_epoch"]) -> None: ...

        LOGIN_NAME_FIELD_NUMBER: builtins.int
        FULL_NAME_FIELD_NUMBER: builtins.int
        GROUPS_FIELD_NUMBER: builtins.int
        LAST_UPDATED_FIELD_NUMBER: builtins.int
        DISABLED_FIELD_NUMBER: builtins.int
        login_name: builtins.str
        full_name: builtins.str
        disabled: builtins.bool
        @property
        def groups(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
        @property
        def last_updated(self) -> global___DetailsResp.UserDetails.DateTime: ...
        def __init__(
            self,
            *,
            login_name: builtins.str = ...,
            full_name: builtins.str = ...,
            groups: collections.abc.Iterable[builtins.str] | None = ...,
            last_updated: global___DetailsResp.UserDetails.DateTime | None = ...,
            disabled: builtins.bool = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["last_updated", b"last_updated"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["disabled", b"disabled", "full_name", b"full_name", "groups", b"groups", "last_updated", b"last_updated", "login_name", b"login_name"]) -> None: ...

    USER_DETAILS_FIELD_NUMBER: builtins.int
    @property
    def user_details(self) -> global___DetailsResp.UserDetails: ...
    def __init__(
        self,
        *,
        user_details: global___DetailsResp.UserDetails | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["user_details", b"user_details"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["user_details", b"user_details"]) -> None: ...

global___DetailsResp = DetailsResp

@typing.final
class ChangePasswordReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        LOGIN_NAME_FIELD_NUMBER: builtins.int
        CURRENT_PASSWORD_FIELD_NUMBER: builtins.int
        NEW_PASSWORD_FIELD_NUMBER: builtins.int
        login_name: builtins.str
        current_password: builtins.str
        new_password: builtins.str
        def __init__(
            self,
            *,
            login_name: builtins.str = ...,
            current_password: builtins.str = ...,
            new_password: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["current_password", b"current_password", "login_name", b"login_name", "new_password", b"new_password"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___ChangePasswordReq.Options: ...
    def __init__(
        self,
        *,
        options: global___ChangePasswordReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["options", b"options"]) -> None: ...

global___ChangePasswordReq = ChangePasswordReq

@typing.final
class ChangePasswordResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ChangePasswordResp = ChangePasswordResp

@typing.final
class ResetPasswordReq(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Options(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        LOGIN_NAME_FIELD_NUMBER: builtins.int
        NEW_PASSWORD_FIELD_NUMBER: builtins.int
        login_name: builtins.str
        new_password: builtins.str
        def __init__(
            self,
            *,
            login_name: builtins.str = ...,
            new_password: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["login_name", b"login_name", "new_password", b"new_password"]) -> None: ...

    OPTIONS_FIELD_NUMBER: builtins.int
    @property
    def options(self) -> global___ResetPasswordReq.Options: ...
    def __init__(
        self,
        *,
        options: global___ResetPasswordReq.Options | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["options", b"options"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["options", b"options"]) -> None: ...

global___ResetPasswordReq = ResetPasswordReq

@typing.final
class ResetPasswordResp(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___ResetPasswordResp = ResetPasswordResp
