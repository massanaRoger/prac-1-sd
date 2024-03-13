import json
import socket

# Redis params
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


def connect_individual_chat(username: str, client_ip='localhost'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        client_port = s.getsockname()[1]

        # Format to register user:
        # ACTION -> REGISTER
        # USERNAME -> user_id
        # ADDRESS -> IP and PORT
        register_message = {
            "action": "REGISTER",
            "username": username,
            "address": {"ip": client_ip, "port": client_port}
        }
        s.sendall(json.dumps(register_message).encode('utf-8'))

        # Wait ACK server
        response = s.recv(1024)
        print(f"Registration response: {response.decode('utf-8')}")


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

        if option == "1":
            # Placeholder for connect to chat functionality
            chat_id = input("Enter chat ID to connect: ")

            connect_individual_chat(username)
            print(f"Connecting to chat {chat_id}...")



        elif option == "2":
            # Placeholder for subscribe to group chat functionality
            chat_id = input("Enter group chat ID to subscribe: ")
            print(f"Subscribing to group chat {chat_id}... (functionality not implemented)")
        elif option == "3":
            # Placeholder for discover chats functionality
            print("Discovering active chats... (functionality not implemented)")
        elif option == "4":
            # Placeholder for access insult channel functionality
            print("Accessing insult channel... (functionality not implemented)")
        elif option == "5":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
