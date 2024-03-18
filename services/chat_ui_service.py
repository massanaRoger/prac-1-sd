import sys
import time

import grpc

from protos import grpc_chat_pb2_grpc, grpc_chat_pb2
from utils import config


def start_chat_server_conn():
    # open a gRPC channel to the chat server
    client_channel = grpc.insecure_channel(config.CHAT_SERVER)

    # create a stub_server (client)
    return grpc_chat_pb2_grpc.MessagingServiceStub(client_channel)


def make_message(sender, reciever, message):
    return grpc_chat_pb2.Message(
        timestamp=int(time.time()),
        sender=sender,
        receiver=reciever,
        content=message
    )


def generate_messages():
    messages = [
        make_message("ME", "YOU", "HELLO WORLD"),
        make_message("YOU", "TO ME", "HELLO WORLD TOO")
    ]

    for msg in messages:
        print(f"'{msg.timestamp}' {msg.sender} said: {msg.content}")
        yield msg


def bidirectional_chat(stub_client):
    responses = stub_client.BidirectionalChat(generate_messages())
    for response in responses:
        print(
            "Received message from %s: %s" % (response.sender, response.content)
        )


def run_chat(stub_client):
    print("-------------- Bidirectional Chat --------------")
    bidirectional_chat(stub_client)


if __name__ == "__main__":
    run_chat(start_chat_server_conn())