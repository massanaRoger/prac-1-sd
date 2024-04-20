import sys
import threading
import time
from datetime import datetime

import grpc

from protos import grpc_chat_pb2_grpc, grpc_chat_pb2


class PrivateChatUI:
    def __init__(self, sender, sender_ip, sender_port, receiver, receiver_ip, receiver_port):
        self.sender = sender
        self.sender_ip = sender_ip
        self.sender_port = sender_port
        self.receiver = receiver
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port

        # Open 2 stubs: 1 for the client and the other to the own server
        # Open stub for the user to chat with
        self.client_1_channel = grpc.insecure_channel(f"{self.sender_ip}:{self.sender_port}")
        self.stub_client_1 = grpc_chat_pb2_grpc.MessagingServiceStub(self.client_1_channel)

        # Open stub for my own server (to receive messages)
        self.client_2_channel = grpc.insecure_channel(f"{self.receiver_ip}:{self.receiver_port}")
        self.stub_client_2 = grpc_chat_pb2_grpc.MessagingServiceStub(self.client_2_channel)

        # Start thread to receive concurrent messages
        self.receive_thread = threading.Thread(target=self.start_receiving_messages, daemon=True)

    # Format the message
    def make_message(self, message):
        msg_time = int(time.time())
        timestamp = datetime.fromtimestamp(msg_time)
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        return grpc_chat_pb2.Message(
            timestamp=formatted_timestamp,
            sender=self.sender,
            content=message
        )

    # Send message
    def send_messages(self):
        # This method handles sending messages to the server
        while True:
            message = None
            while message is None or message.strip() == "":
                message = input("")
            message_request = self.make_message(message)
            self.stub_client_2.SendMessage(message_request)

    # Thread to recevie messages constantly
    def start_receiving_messages(self):
        try:
            for msg in self.stub_client_1.StreamMessages(grpc_chat_pb2.google_dot_protobuf_dot_empty__pb2.Empty()):
                if msg.sender == self.receiver:
                    print(f"'{msg.timestamp}' Message from '{msg.sender}': {msg.content}")
        except grpc.RpcError as err:
            print(f"Disconnected")
            print(err.args)
            print(err)

    # Main thread
    def run_chat(self):
        print("-------------- CHAT UI --------------")
        self.receive_thread.start()

        try:
            self.send_messages()
        except KeyboardInterrupt:
            print("Chat ended")
            self.client_1_channel.close()
            self.client_2_channel.close()


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: python chat_ui_service.py [sender name] [sender IP] [sender port] [receiver name] [receiver IP] "
              "[receiver port]")
        print("Length:", len(sys.argv))
        time.sleep(2)
    else:
        chat_ui = PrivateChatUI(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        print("CLIENT 1: ", sys.argv[1])
        print("CLIENT 1 IP: ", sys.argv[2])
        print("CLIENT 1 PORT: ", sys.argv[3])
        print("CLIENT 2: ", sys.argv[4])
        print("CLIENT 2 IP: ", sys.argv[5])
        print("CLIENT 2 PORT: ", sys.argv[6])

        chat_ui.run_chat()
