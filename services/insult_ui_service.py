import sys
import threading
import time
import traceback
from datetime import datetime

import pika

CHAT_NAME = "INSULT_CHAT"


class InsultChatUI:
    def __init__(self):
        # RabbitMQ queue and exhcange names
        self.queue_name = f'insult_chat_queue'

        # Start thread to receive concurrent messages
        self.receive_thread = threading.Thread(target=self.start_receiving_messages, daemon=True)

    def __del__(self):
        self.receive_thread.join()

    def setup_chat_queue(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        # Create a unique queue for each client
        channel.queue_declare(queue=self.queue_name, durable=True)

        return channel

    def make_message(self, message):
        msg_time = int(time.time())
        timestamp = datetime.fromtimestamp(msg_time)
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        return f"{formatted_timestamp}: {message}"

    def send_messages(self):
        # Set up the queue for this chat_id
        channel = self.setup_chat_queue()

        while True:
            message = input("")
            formatted_message = self.make_message(message)
            channel.basic_publish(exchange='', routing_key=self.queue_name,
                                  body=formatted_message.encode())

    def start_receiving_messages(self):
        def callback(ch, method, properties, body):
            print("INSULTED! -> ", body.decode())

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
        print("INSULT CHAT UI\n")
        self.receive_thread.start()

        try:
            self.send_messages()
        except KeyboardInterrupt:
            print("Chat ended")
        except Exception as e:
            print(e)
            time.sleep(10)


if __name__ == "__main__":
    chat_ui = InsultChatUI()
    chat_ui.run_chat()
