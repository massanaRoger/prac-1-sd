import subprocess
import grpc
import time

from protos import grpc_chat_pb2_grpc

from protos import grpc_chat_pb2


class MessagingServiceServicer(grpc_chat_pb2_grpc.MessagingServiceServicer):

    def __init__(self):
        self.messages = []

    def RequestConnection(self, request, context):
        try:
            # Create reciever terminal
            # Client 1 - SENDER
            # Client 2 - RECEIVER
            subprocess.Popen([
                "gnome-terminal", "--", "bash", "-c",
                f"python3 ../services/chat_ui_service.py {request.client_1} {request.client_1_ip} {request.client_1_port} {request.client_2} {request.client_2_ip} {request.client_2_port} exec bash"
            ])
            return grpc_chat_pb2.ConnectionStatusReply(status=True)
        except grpc.RpcError as err:
            print(f"User {request.client_2} is disconnected!")
            return grpc_chat_pb2.ConnectionStatusReply(status=False)

    def SendMessage(self, request, context):
        message = {
            "timestamp": request.timestamp,
            "sender": request.sender,
            "content": request.content
        }
        self.messages.append(message)
        return request

    def StreamMessages(self, request, context):
        last_index = 0
        while True:
            while len(self.messages) > last_index:
                message = self.messages[last_index]
                last_index += 1
                yield grpc_chat_pb2.Message(timestamp=message["timestamp"], sender=message["sender"], content=message["content"])
            time.sleep(0.5)
