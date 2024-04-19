import threading
import time
import traceback

import pika

from utils.utilities import start_redis_server_conn, delete_user_from_group


class Discovery:

    def __init__(self, name, is_group):
        self.channel = None
        self.name = name
        self.is_group = is_group
        self.connection = None
        self.discovery_exchange = "discovery_exchange"
        self.queue = f"{name}_discovery_event_queue"
        self.receive_thread = threading.Thread(target=self.start_receiving_discovery_events, daemon=True)
        self.stub = start_redis_server_conn()

    def __del__(self):
        self.receive_thread.join()
        self.connection.close()

    # Creates a queue for each connected client
    def setup_discovery_user_queue(self):
        # Create connection to RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        # Declare a fanout exchange (fanout = msg to all users)
        self.channel.exchange_declare(exchange=self.discovery_exchange, exchange_type='fanout')

        # Create a unique queue for each client
        self.channel.queue_declare(queue=self.queue, durable=True)

        # Bind this client's unique queue to the exchange
        self.channel.queue_bind(exchange=self.discovery_exchange, queue=self.queue)

    def start_receiving_discovery_events(self):
        def callback(ch, method, properties, body):
            if body.decode() == 'remove_user' and self.is_group:
                print("Removed user")
                # Call remove_user servicer
                group = delete_user_from_group(self.stub, self.name)
                if group.num_users == 0:
                    self.connection.close()

            username = body.decode()
            if self.name not in username:

                # Send username to discover client
                if self.is_group:
                    self.channel.basic_publish(exchange='',
                                               routing_key=f"{username}_discover_queue",
                                               body="Group: " + self.name)
                else:
                    self.channel.basic_publish(exchange='',
                                               routing_key=f"{username}_discover_queue",
                                               body="User: " + self.name)
                # print("Discover message:", body.decode())

        try:
            self.setup_discovery_user_queue()
            self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

        except Exception as e:
            self.connection.close()
            print("Error encountered:", e)
            traceback.print_exc()
            time.sleep(10000)
