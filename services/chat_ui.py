import sys


def run_chat(user_chat_id, user_2):
    messages = []

    print(f"Welcome to the chat, {user_chat_id}! You're now chatting with {user_2}.")
    print("Type 'exit' to leave the chat.\n")

    while True:
        # Display existing messages
        for message in messages:
            print(message)

        # Get input from the user
        user_message = input(f"{user_chat_id}: ")

        # Check if the user wants to exit
        if user_message.lower() == 'exit':
            print("Exiting chat.")
            break

        # Add the user's message to the chat history
        messages.append(f"{user_chat_id}: {user_message}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python chat_ui.py [your name] [other person's name]")
    else:
        your_name = sys.argv[1]
        other_name = sys.argv[2]
        run_chat(your_name, other_name)
