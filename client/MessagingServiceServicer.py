import time

from protos import grpc_chat_pb2_grpc

from protos import grpc_chat_pb2


class MessagingServiceServicer(grpc_chat_pb2_grpc.MessagingServiceServicer):

    def BidirectionalChat(self, request_iterator, context):
        for new_note in request_iterator:
            yield new_note
