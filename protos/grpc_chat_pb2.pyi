from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Message(_message.Message):
    __slots__ = ("timestamp", "sender", "receiver", "content")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    sender: str
    receiver: str
    content: str
    def __init__(self, timestamp: _Optional[int] = ..., sender: _Optional[str] = ..., receiver: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...
