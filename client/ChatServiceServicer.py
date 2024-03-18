import time

from protos import grpc_chat_pb2_grpc

from protos import grpc_chat_pb2


class ChatServiceServicer(grpc_chat_pb2_grpc.MessagingServiceServicer):

    def __init__(self):
        self.chat_service = XXX

    def BidirectionalChat(self, request_iterator, context):
        prev_notes = []
        for new_note in request_iterator:
            for prev_note in prev_notes:
                yield prev_note
            prev_notes.append(new_note)