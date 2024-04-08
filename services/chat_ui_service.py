import sys
import time
from datetime import datetime

import grpc

from protos import grpc_chat_pb2_grpc, grpc_chat_pb2
from utils import config


class ChatUI:
    def __init__(self, sender, receiver, receiver_ip, receiver_port):
        self.sender = sender
        self.receiver = receiver
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.stub_client = self.start_chat_server_conn()

    def start_chat_server_conn(self):
        # open a gRPC channel to the client 2
        client_channel = grpc.insecure_channel(f"{self.receiver_ip}:{self.receiver_port}")
        # create a stub_server (client 2)
        return grpc_chat_pb2_grpc.MessagingServiceStub(client_channel)

    # Format of the user messages
    def make_message(self, message):
        message_request = grpc_chat_pb2.Message(
            timestamp=int(time.time()),
            sender=self.sender,
            content=message
        )
        self.stub_client.BidirectionalChat(message_request)

        return message_request

    # User input
    def generate_messages(self):
        while True:
            message = input(f"")
            yield self.make_message(message)

    def receive_messages(self, stub_client):
        for msg in stub_client.BidirectionalChat(self.generate_messages()):
            timestamp = datetime.fromtimestamp(msg.timestamp)
            formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            print(f"'{formatted_timestamp}' Message from '{msg.sender}': {msg.content}")

            

    def run_chat(self):
        print("-------------- CHAT UI --------------")
        self.receive_messages(self.stub_client)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python chat_ui_service.py [sender name] [receiver name] [receiver IP] [receiver port]")
        print("Length:", len(sys.argv))
        time.sleep(2)
    else:
        chat_ui = ChatUI(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        print("ME: ", sys.argv[1])
        print("USER: ", sys.argv[2])
        print("USER IP: ", sys.argv[3])
        print("USER PORT: ", sys.argv[4])
        chat_ui.run_chat()
