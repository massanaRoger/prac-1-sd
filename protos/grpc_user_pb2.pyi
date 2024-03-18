from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterMessageRequest(_message.Message):
    __slots__ = ("username", "ip", "port")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    username: str
    ip: str
    port: int
    def __init__(self, username: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class RegisterMessageReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class LookupUserRequest(_message.Message):
    __slots__ = ("username",)
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    def __init__(self, username: _Optional[str] = ...) -> None: ...

class LookupUserReply(_message.Message):
    __slots__ = ("status", "username", "ip", "port")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    status: bool
    username: str
    ip: str
    port: int
    def __init__(self, status: bool = ..., username: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class SendMessageRequest(_message.Message):
    __slots__ = ("sender_username", "receiver_username", "message")
    SENDER_USERNAME_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_USERNAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    sender_username: str
    receiver_username: str
    message: str
    def __init__(self, sender_username: _Optional[str] = ..., receiver_username: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class SendMessageReplay(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    def __init__(self, success: bool = ..., error: _Optional[str] = ...) -> None: ...
