from concurrent import futures
import redis
import grpc
import threading

from client.MessagingServiceServicer import MessagingServiceServicer
from utils import config

from protos import grpc_user_pb2_grpc
from UserServiceServicer import UserServiceServicer

from protos import grpc_chat_pb2_grpc


# create a class to define the server functions, derived from
# grpc_chat_pb2_grpc.ChatServiceServicer

def create_redis_connection():
    # Create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    # use the generated function `add_ChatServiceServicer_to_server`
    # to add the defined class to the server
    grpc_user_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(redis_client), server)

    # Listen to port 50051
    print('Starting Redis server... Listening on port 50051.')
    server.add_insecure_port(config.REDIS_SERVER)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    thread_grpc = threading.Thread(target=create_redis_connection)

    # Start both servers
    thread_grpc.start()

    # Wait to kill processes
    thread_grpc.join()
