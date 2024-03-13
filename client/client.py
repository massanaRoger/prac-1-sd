import json
import socket
import grpc

from protos import grpc_chat_pb2
from protos import grpc_chat_pb2_grpc

# Redis params
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')


# Get unused port to stablish communication between hosts
def get_unused_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    _, port = s.getsockname()
    s.close()
    return port


def main():
    print("Welcome to the Chat Application!")
    username = input("Enter your username: ")

    print(f"Hello, {username}! What would you like to do?")

    while True:
        print("\nOptions:")
        print("1. Connect to a chat by specifying its ID.")
        print("2. Subscribe to a group chat by specifying its ID.")
        print("3. Discover active chats.")
        print("4. Access insult channel.")
        print("5. Exit.")

        option = input("Please choose an option (1-5): ")

        # 1. Connect chat (private or group)
        if option == "1":
            chat_id = input("Enter chat ID to connect (1-100): ")
            if 0 < int(chat_id) <= 10:
                print("Entering private chat...")
                # create a stub (client)
                stub = grpc_chat_pb2_grpc.ChatServiceStub(channel)

                # create a register message
                register_message = grpc_chat_pb2.RegisterMessageRequest(chat_id=chat_id, username=username,
                                                                       ip='localhost', port=get_unused_port())
                stub.RegisterUser(register_message)

            elif 10 < int(chat_id) <= 100:
                print("Entering group chat...")


        elif option == "2":
            chat_id = input("Enter group chat ID to subscribe: ")
            print(f"Subscribing to group chat {chat_id}... (functionality not implemented)")
        elif option == "3":
            print("Discovering active chats... (functionality not implemented)")
        elif option == "4":
            print("Accessing insult channel... (functionality not implemented)")
        elif option == "5":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
