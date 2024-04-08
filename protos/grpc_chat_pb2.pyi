from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectionMessageRequest(_message.Message):
    __slots__ = ("sender", "receiver", "ip", "port")
    SENDER_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    receiver: str
    ip: str
    port: int
    def __init__(self, sender: _Optional[str] = ..., receiver: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class ConnectionStatusReply(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: bool
    def __init__(self, status: bool = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("timestamp", "sender", "content")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    sender: str
    content: str
    def __init__(self, timestamp: _Optional[int] = ..., sender: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...
