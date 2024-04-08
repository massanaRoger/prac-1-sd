import sys
import threading
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
        self.client_channel = grpc.insecure_channel(f"{self.receiver_ip}:{self.receiver_port}")
        self.stub_client = grpc_chat_pb2_grpc.MessagingServiceStub(self.client_channel)
        self.receive_thread = threading.Thread(target=self.start_receiving_messages, daemon=True)

    def make_message(self, message):
        # This method now only creates a message object, doesn't send it
        return grpc_chat_pb2.Message(
            timestamp=int(time.time()),
            sender=self.sender,
            content=message
        )

    def generate_messages(self):
        while True:
            message = input("")
            yield self.make_message(message)

    def send_messages(self, messages):
        # This method handles sending messages to the server
        for message in messages:
            self.stub_client.BidirectionalChat(iter([message]))
            print("Message sent")

    def start_receiving_messages(self):
        try:
            for msg in self.stub_client.BidirectionalChat(iter([])):
                print("Message received")
                timestamp = datetime.fromtimestamp(msg.timestamp)
                formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                print(f"'{formatted_timestamp}' Message from '{msg.sender}': {msg.content}")
        except grpc.RpcError as err:
            print(f"Disconnected")

    def run_chat(self):
        print("-------------- CHAT UI --------------")
        self.receive_thread.start()

        try:
            self.send_messages(self.generate_messages())
        except KeyboardInterrupt:
            print("Chat ended")
            self.client_channel.close()


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
