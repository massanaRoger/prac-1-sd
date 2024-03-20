import sys
import time

import grpc

from protos import grpc_chat_pb2_grpc, grpc_chat_pb2
from utils import config


class ChatUI:
    def __init__(self):
        self.sender = None
        self.sender_ip = None
        self.sender_port = None
        self.receiver = None

    def start_chat_server_conn(self):
        # open a gRPC channel to the chat server
        client_channel = grpc.insecure_channel(config.CHAT_SERVER)
        # create a stub_server (client)
        return grpc_chat_pb2_grpc.MessagingServiceStub(client_channel)

    # Format of the user messages
    def make_message(self, message):
        return grpc_chat_pb2.Message(
            timestamp=int(time.time()),
            sender=self.sender,
            receiver=self.receiver,
            content=message
        )

    # User input
    def generate_messages(self):
        while True:
            message = input("YOU: ")
            yield self.make_message(message)

    def receive_messages(self, stub_client):
        for msg in stub_client.BidirectionalChat(self.generate_messages()):
            print(f"Received message from {msg.sender}: {msg.content}")

    def run_chat(self):
        print("-------------- CHAT UI --------------")
        stub_client = self.start_chat_server_conn()
        self.receive_messages(stub_client)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python chat_ui_service.py [your name] [your IP] [other person's name] [your port]")
    else:
        chat_ui = ChatUI()
        chat_ui.sender = sys.argv[1]
        chat_ui.sender_ip = sys.argv[2]
        chat_ui.sender_port = sys.argv[4]
        chat_ui.receiver = sys.argv[3]
        chat_ui.run_chat()
