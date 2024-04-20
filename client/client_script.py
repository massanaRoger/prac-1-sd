import subprocess
import threading

import discovery
from protos import grpc_chat_pb2
from utils.utilities import *


def main():
    # Start Redis server connection
    stub_server = start_redis_server_conn()

    # Init chat application
    print("Welcome to the Chat Application!")
    username = None
    while username is None or username.strip() == "":
        username = input("Enter your username: ")
    print(f"Hello, {username}! What would you like to do?")

    # Create a queue to receive 'discover' messages
    discovery_channel = discovery.Discovery(username, is_group=False)
    discovery_channel.receive_thread.start()

    # Lookup if user already exists
    sender_details = lookup_user(stub_server, username)
    # If user doesn't exist, register to Re
    if sender_details.status is False:
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
                chat_id = input("Enter the name of the client to connect: ")
                receiver_details = lookup_user(stub_server, chat_id)

                if receiver_details.status is False:
                    print("User doesn't exist!")
                    continue

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
                    continue

                # Open dedicated terminal for the chat (from client 1 (this) to client 2)
                # Usage: python chat_ui_service.py [sender name] [receiver name] [receiver IP] [receiver port]
                subprocess.Popen([
                    "gnome-terminal", "--", "bash", "-c",
                    f"python3 ../services/chat_ui_service.py {sender_details.username} {sender_details.ip} {sender_details.port} {receiver_details.username} {receiver_details.ip} {receiver_details.port} exec bash"
                ])

            elif option == "2":
                chat_id = None
                while chat_id is None or chat_id.strip() == "":
                    chat_id = input("Enter group name to subscribe: ")

                # Look up if the group name already exists in Redis
                group_exists = lookup_group(stub_server, chat_id)
                if group_exists.status is False:
                    # Register group chat to Redis if not done yet
                    group_chat_details = register_group(stub_server, chat_id)
                    print("GROUP REGISTER: ", group_chat_details)
                else:
                    add_user_to_group(stub_server, chat_id)

                print("GROUP LOOKUP: ", group_exists)

                print("Entering group chat...")
                subprocess.Popen([
                    "gnome-terminal", "--", "bash", "-c",
                    f"python3 ../services/group_ui_service.py {sender_details.username} {chat_id} exec bash"
                ])

            elif option == "3":
                print("Discovering active chats... Please wait")
                # 1. Creates receiving queue
                # 2. Send discover messages
                # 3. Receive discovered clients
                # 4. Join discover thread
                discover_thread = threading.Thread(target=start_receiving_discovered_clients,
                                                   args=[username], daemon=False)
                discover_thread.start()
                # 4. Join discover thread
                discover_thread.join()

            elif option == "4":
                print("Entering insult chat...")
                subprocess.Popen([
                    "gnome-terminal", "--", "bash", "-c",
                    f"python3 ../services/insult_ui_service.py exec bash"
                ])

            elif option == "5":
                print("Exiting the application. Goodbye!")
                remove_user(stub_server, username)
                return
            else:
                print("Invalid option. Please try again.")
        else:
            time.sleep(1)  # Wait for the chat to finish

    # Kill threads
    chat_server_thread.join()


if __name__ == "__main__":
    main()
