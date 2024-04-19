import socket
import time
from concurrent import futures

import grpc
import pika

from client import MessagingServiceServicer
from protos import grpc_user_pb2, grpc_chat_pb2_grpc, grpc_user_pb2_grpc
from utils import config


# Connect to Redis server
def start_redis_server_conn():
    # open a gRPC channel to the server
    channel = grpc.insecure_channel(config.REDIS_SERVER)
    # create a stub_server (client)
    stub_server = grpc_user_pb2_grpc.UserServiceStub(channel)
    return stub_server


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
    # Create a register message
    register_message = grpc_user_pb2.RegisterUserMessageRequest(username=username,
                                                                ip='localhost', port=get_unused_port())
    stub.RegisterUser(register_message)
    return register_message


def lookup_user(stub, username):
    lookup_message = grpc_user_pb2.LookupUserRequest(username=username)
    return stub.LookupUser(lookup_message)


def register_group(stub, group_name):
    # create a register group message
    register_message = grpc_user_pb2.RegisterGroupMessageRequest(group_name=group_name)
    message = stub.RegisterGroup(register_message)
    # print(message.message)
    return register_message


def lookup_group(stub, group_name):
    lookup_message = grpc_user_pb2.LookupGroupRequest(group_name=group_name)
    result = stub.LookupGroup(lookup_message)
    return result


def add_user_to_group(stub, group_name):
    user_to_group = grpc_user_pb2.LookupGroupRequest(group_name=group_name)
    return stub.AddUserToGroup(user_to_group)


def delete_user_from_group(stub, group_name):
    deleted_user = grpc_user_pb2.LookupGroupRequest(group_name=group_name)
    return stub.DeleteUserFromGroup(deleted_user)


def start_receiving_discovered_clients(username):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    try:
        discover_channel = connection.channel()
        discover_channel.queue_declare(queue=f'{username}_discover_queue')

        discover_channel.basic_publish(exchange='discovery_exchange',
                                       routing_key='',
                                       body=username)

        def callback(ch, method, properties, body):
            print(body.decode())

        discover_channel.basic_consume(queue=f'{username}_discover_queue', on_message_callback=callback, auto_ack=True)

        # Handle events for 3 seconds. This blocks and processes incoming messages or other events.
        # Start time for the timeout
        start_time = time.time()
        timeout_seconds = 3  # Timeout after 3 seconds

        while True:
            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout_seconds:
                break
            connection.process_data_events(time_limit=1)  # Process events for 1 second

        print("Timeout reached or done processing events, stopping consuming.")
        discover_channel.stop_consuming()

    except Exception as e:
        print("Error during consuming:", e)
    finally:
        if connection.is_open:
            connection.close()
