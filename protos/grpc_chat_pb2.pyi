from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectionMessageRequest(_message.Message):
    __slots__ = ("client_1", "client_1_ip", "client_1_port", "client_2", "client_2_ip", "client_2_port")
    CLIENT_1_FIELD_NUMBER: _ClassVar[int]
    CLIENT_1_IP_FIELD_NUMBER: _ClassVar[int]
    CLIENT_1_PORT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_2_FIELD_NUMBER: _ClassVar[int]
    CLIENT_2_IP_FIELD_NUMBER: _ClassVar[int]
    CLIENT_2_PORT_FIELD_NUMBER: _ClassVar[int]
    client_1: str
    client_1_ip: str
    client_1_port: int
    client_2: str
    client_2_ip: str
    client_2_port: int
    def __init__(self, client_1: _Optional[str] = ..., client_1_ip: _Optional[str] = ..., client_1_port: _Optional[int] = ..., client_2: _Optional[str] = ..., client_2_ip: _Optional[str] = ..., client_2_port: _Optional[int] = ...) -> None: ...

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
    timestamp: str
    sender: str
    content: str
    def __init__(self, timestamp: _Optional[str] = ..., sender: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...
