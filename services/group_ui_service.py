import os
import signal
import sys
import threading
import time
import traceback
from datetime import datetime

import pika


class GroupChatUI:
    def __init__(self, sender, chat_id):
        self.sender = sender
        self.chat_id = chat_id

        # RabbitMQ queue and exhcange names
        self.queue_name = f'chat_{self.chat_id}_{self.sender}'
        self.exchange_name = f'group_chat_{self.chat_id}_exchange'
        self.discovery_event_queue = f'{self.chat_id}_discovery_event_queue'

        # Start thread to receive concurrent messages
        self.receive_thread = threading.Thread(target=self.start_receiving_messages, daemon=True)

    def cleanup(self):
        print("Cleaning")
        time.sleep(5)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.basic_publish(exchange='',
                              routing_key=self.discovery_event_queue,
                              body="remove_user")
        # self.receive_thread.join()
        os.system('kill $$')


    def setup_chat_queue(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a fanout exchange
        channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')

        # Create a unique queue for each client
        channel.queue_declare(queue=self.queue_name, durable=True)

        # Bind this client's unique queue to the exchange
        channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)

        return channel

    def make_message(self, message):
        msg_time = int(time.time())
        timestamp = datetime.fromtimestamp(msg_time)
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        return f"{formatted_timestamp} from {self.sender}: {message}"

    def send_messages(self):
        # Set up the queue for this chat_id
        channel = self.setup_chat_queue()

        while True:
            message = input("")
            formatted_message = self.make_message(message)
            channel.basic_publish(exchange=self.exchange_name, routing_key=self.chat_id,
                                  body=formatted_message.encode())

            print("Message sent!")

    def start_receiving_messages(self):
        def callback(ch, method, properties, body):
            if self.sender not in body.decode():
                print("Message received:", body.decode())

            if "exit" in body.decode():
                self.cleanup()

        try:
            # Set up the queue for this chat_id
            channel = self.setup_chat_queue()

            channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
            channel.start_consuming()

        except Exception as e:
            print("Error encountered:", e)
            traceback.print_exc()
            time.sleep(10000)

    def run_chat(self):
        print("CHAT UI\n")
        self.receive_thread.start()

        try:
            self.send_messages()
        except KeyboardInterrupt:
            print("Chat ended")
        except Exception as e:
            print(e)
            time.sleep(10)


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: python chat_ui_service.py [sender name] [chat ID]")
    else:
        chat_ui = GroupChatUI(sys.argv[1], sys.argv[2])
        chat_ui.run_chat()
