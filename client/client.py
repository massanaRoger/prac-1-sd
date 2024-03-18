import socket
import grpc
import subprocess
import time
from concurrent import futures

from exceptions.private_chat_exception import PrivateChatException
from protos import grpc_user_pb2
from protos import grpc_user_pb2_grpc
from services.user_service import UserService

# Redis params
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


# Get unused port to stablish communication between hosts
def get_unused_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    _, port = s.getsockname()
    s.close()
    return port


def run_chat_ui(chat_id, username):
    print(f"Starting chat UI for user: {username}...")

    terminal_command = f"python3 ../services/chat_ui.py {chat_id} {username} {port}; exec bash"
    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", terminal_command])
    time.sleep(2)


def register_user(stub, username):
    # create a register message
    register_message = grpc_user_pb2.RegisterMessageRequest(username=username,
                                                            ip='localhost', port=get_unused_port())
    message = stub.RegisterUser(register_message)
    # print(message.message)
    return register_message


def create_client_channel(ip, port):
    client_server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

    client_channel = grpc.insecure_channel(f"{ip}:{port}")
    client_server.start()

    return client_channel


def main():
    # open a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')

    print("Welcome to the Chat Application!")
    username = input("Enter your username: ")

    print(f"Hello, {username}! What would you like to do?")

    # create a stub (client)
    stub = grpc_user_pb2_grpc.UserServiceStub(channel)

    # Register user before entering to the chat appication logic
    user_details = {
        "username": "",
        "ip": "",
        "port": 0
    }

    try:
        user_details = register_user(stub, username)
    except PrivateChatException as p:
        print(f"ERROR! {username} is alredy chating!")

    in_chat = False  # Flag to indicate if the user is in a chat

    is_server_created = False
    while True:
        if not in_chat:
            print("\nOptions:")
            print("1. Connect to a chat by specifying its ID.")
            print("2. Subscribe to a group chat by specifying its ID.")
            print("3. Discover active chats.")
            print("4. Access insult channel.")
            print("5. Exit.")

            option = input("Please choose an option (1-5): ")

            # 1. Connect chat (private or group)
            if option == "1":
                chat_type_correct = False
                while not chat_type_correct:
                    chat_type = input(
                        "Do you want to enter to a private chat or a group chat? Enter '1' for private chat "
                        "or '2' for group chat: ")
                    if chat_type == '1':

                        # 1. Create dedicated server for the user
                        if not is_server_created:
                            print(f"Creating server for user '{username}'...")
                            create_client_channel(user_details.ip, user_details.port)
                            print(f"Server created!")
                            is_server_created = True

                        # 2. Lookup user to chat with
                        chat_type_correct = True
                        user_to_chat = input("Enter the name of the username to connect: ")
                        lookup_message = grpc_user_pb2.LookupUserRequest(username=user_to_chat)
                        user_params = stub.LookupUser(lookup_message)

                        if user_params.status is False:
                            print("User doesn't exist!")
                            break

                        print(f"User '{user_params.username}' found!")
                        # 4. Start chat
                        #run_chat_ui(user_to_chat, username)


                    elif chat_type == '2':
                        chat_type_correct = True
                        user_to_chat = input("Enter the name of the group to connect: ")
                        print("Entering group chat...")




            elif option == "2":
                user_to_chat = input("Enter group chat ID to subscribe: ")
                print(f"Subscribing to group chat {user_to_chat}... (functionality not implemented)")
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


if __name__ == "__main__":
    main()
