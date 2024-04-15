import sys
import threading
import time
from datetime import datetime

import pika


class GroupChatUI:
    def __init__(self, sender, chat_id):
        self.sender = sender
        self.chat_id = chat_id
        self.queue_name = ""

        # Setup RabbitMQ connection and channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        # Declare the exchange
        self.exchange_name = 'group_chat_exchange'
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='topic')

        # Setup the queue for this chat_id
        self.setup_chat_queue()

        # Start thread to receive concurrent messages
        self.receive_thread = threading.Thread(target=self.start_receiving_messages, daemon=True)

    def setup_chat_queue(self):
        self.queue_name = f'chat_{self.chat_id}'
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=self.chat_id)

    def make_message(self, message):
        msg_time = int(time.time())
        timestamp = datetime.fromtimestamp(msg_time)
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        return f"{formatted_timestamp} {self.sender}: {message}"

    def send_messages(self):
        while True:
            message = input("")
            formatted_message = self.make_message(message)
            self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.chat_id,
                                       body=formatted_message.encode())

            print("Message sent!")

    def start_receiving_messages(self):
        def callback(ch, method, properties, body):
            print("Message received:", body.decode())

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def run_chat(self):
        print("-------------- CHAT UI --------------")
        self.receive_thread.start()

        try:
            self.send_messages()
        except KeyboardInterrupt:
            print("Chat ended")
            self.connection.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python chat_ui_service.py [sender name] [chat ID]")
    else:
        chat_ui = GroupChatUI(sys.argv[1], sys.argv[2])
        chat_ui.run_chat()
