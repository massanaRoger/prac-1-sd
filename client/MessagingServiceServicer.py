import subprocess

from protos import grpc_chat_pb2_grpc

from protos import grpc_chat_pb2


class MessagingServiceServicer(grpc_chat_pb2_grpc.MessagingServiceServicer):

    def BidirectionalChat(self, request_iterator, context):
        for new_note in request_iterator:
            yield new_note

    def RequestConnection(self, request, context):

        # Create reciever terminal
        subprocess.Popen([
            "gnome-terminal", "--", "bash", "-c",
            f"python3 ../services/chat_ui_service.py {request.name} {request.ip} {request.port} exec bash"
        ])
        return grpc_chat_pb2.ConnectionStatusReply(status=True)
