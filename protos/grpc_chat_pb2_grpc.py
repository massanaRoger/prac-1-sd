# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import grpc_chat_pb2 as grpc__chat__pb2


class ChatServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.chat = channel.stream_stream(
                '/ChatService/chat',
                request_serializer=grpc__chat__pb2.ChatMessage.SerializeToString,
                response_deserializer=grpc__chat__pb2.ChatMessage.FromString,
                )


class ChatServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def chat(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'chat': grpc.stream_stream_rpc_method_handler(
                    servicer.chat,
                    request_deserializer=grpc__chat__pb2.ChatMessage.FromString,
                    response_serializer=grpc__chat__pb2.ChatMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ChatService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def chat(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/ChatService/chat',
            grpc__chat__pb2.ChatMessage.SerializeToString,
            grpc__chat__pb2.ChatMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
