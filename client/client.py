import socket
import threading

import grpc
import subprocess
import time
from utils import config
from concurrent import futures

from exceptions.private_chat_exception import PrivateChatException
from protos import grpc_user_pb2, grpc_user_pb2_grpc, grpc_chat_pb2, grpc_chat_pb2_grpc
import MessagingServiceServicer

from protos import grpc_chat_pb2
import multiprocessing


# Connect to Redis server
def start_redis_server_conn():
    # open a gRPC channel to the server
    channel = grpc.insecure_channel(config.REDIS_SERVER)
    # create a stub_server (client)
    stub_server = grpc_user_pb2_grpc.UserServiceStub(channel)
    return stub_server


# Connect to a group chat using RabbitMQ
def connect_group_chat():
    return 0


# Start individual chat server
def start_private_chat_server(ip, port):
    individual_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # use the generated function `add_MessagingServiceServicer_to_server`
    # to add the defined class to the server
    grpc_chat_pb2_grpc.add_MessagingServiceServicer_to_server(
        MessagingServiceServicer.MessagingServiceServicer(), individual_server)

    print(f'\nStarting chat server... Listening on port {port}.')
    individual_server.add_insecure_port(f"{ip}:{port}")
    individual_server.start()
    individual_server.wait_for_termination()


# Get unused port to establish communication between hosts
def get_unused_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    _, port = s.getsockname()
    s.close()
    return port


# Register user to Redis server
def register_user(stub, username):
    # create a register message
    register_message = grpc_user_pb2.RegisterMessageRequest(username=username,
                                                            ip='localhost', port=get_unused_port())
    message = stub.RegisterUser(register_message)
    # print(message.message)
    return register_message


def main():
    # Start Redis server connection
    stub_server = start_redis_server_conn()

    # Init chat application
    print("Welcome to the Chat Application!")
    username = input("Enter your username: ")
    print(f"Hello, {username}! What would you like to do?")

    # Register user before entering to the chat appication logic
    sender_details = {
        "username": "",
        "ip": "",
        "port": 0
    }

    # Register user to Redis
    sender_details = register_user(stub_server, username)

    # Start individual chat server
    chat_server_thread = threading.Thread(target=start_private_chat_server,
                                          args=(sender_details.ip, sender_details.port))
    chat_server_thread.start()
    time.sleep(1)

    in_chat = False  # Flag to indicate if the user is in a chat

    is_server_created = False
    while True:
        if not in_chat:
            print("\nOptions:")
            print("1. Connect to a private chat by specifying its ID.")
            print("2. Subscribe and connect to a group chat by specifying its ID.")
            print("3. Discover active chats.")
            print("4. Access insult channel.")
            print("5. Exit.")

            option = input("Please choose an option (1-5): ")

            # 1. Connect chat (private or group)
            if option == "1":
                chat_id = input("Enter the name of the username to connect: ")
                lookup_message = grpc_user_pb2.LookupUserRequest(username=chat_id)
                receiver_details = stub_server.LookupUser(lookup_message)

                if receiver_details.status is False:
                    print("User doesn't exist!")
                    break

                print(f"User '{receiver_details.username}' found!")
                print("Requesting connection...")

                # Format request message connection
                request_conn_message = grpc_chat_pb2.ConnectionMessageRequest(
                    client_1=receiver_details.username,
                    client_1_ip=receiver_details.ip,
                    client_1_port=receiver_details.port,
                    client_2=sender_details.username,
                    client_2_ip=sender_details.ip,
                    client_2_port=sender_details.port)

                # Create stub to the user to chat with
                stub_connection = grpc_chat_pb2_grpc.MessagingServiceStub(
                    grpc.insecure_channel(f"{receiver_details.ip}:{receiver_details.port}"))

                # Try to create connection to the client (from client 2 to client 1, this)
                connection_details = stub_connection.RequestConnection(request_conn_message)

                if connection_details.status is False:
                    print("Connection refused!")
                    break

                # Open dedicated terminal for the chat (from client 1 (this) to client 2)
                # Usage: python chat_ui_service.py [sender name] [receiver name] [receiver IP] [receiver port]
                subprocess.Popen([
                    "gnome-terminal", "--", "bash", "-c",
                    f"python3 ../services/chat_ui_service.py {sender_details.username} {sender_details.ip} {sender_details.port} {receiver_details.username} {receiver_details.ip} {receiver_details.port} exec bash"
                ])

            elif option == "2":
                chat_id = input("Enter group name to subscribe: ")
                print("Entering group chat...")
                subprocess.Popen([
                    "gnome-terminal", "--", "bash", "-c",
                    f"python3 ../services/group_ui_service.py {sender_details.username} {chat_id} exec bash"
                ])

            elif option == "3":
                print("Discovering active chats... (functionality not implemented)")
            elif option == "4":
                print("Accessing insult channel... (functionality not implemented)")
            elif option == "5":
                print("Exiting the application. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
        else:
            time.sleep(1)  # Wait for the chat to finish

    # Kill threads
    chat_server_thread.join()


if __name__ == "__main__":
    main()
