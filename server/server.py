from concurrent import futures
import redis
import grpc

from protos import grpc_user_pb2_grpc

from services.user_service import UserService


# create a class to define the server functions, derived from
# grpc_chat_pb2_grpc.ChatServiceServicer
class ChatServiceServicer(grpc_user_pb2_grpc.UserServiceServicer):
    def __init__(self, redis_client):
        self.chat_service = UserService(redis_client)

    def RegisterUser(self, register_msg_request, context):
        # Make register request and save the reply to the variable user_message
        user_message = self.chat_service.register_user(register_msg_request.username,
                                                       register_msg_request.ip, register_msg_request.port)

        print("LOG: ", user_message.message)
        return user_message

    def LookupUser(self, request, context):
        user = self.chat_service.lookup_user(request.username)

        print(f"LOG: {user.username} registered")
        return user


def create_grpc_connection():
    # Create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    # use the generated function `add_ChatServiceServicer_to_server`
    # to add the defined class to the server
    grpc_user_pb2_grpc.add_UserServiceServicer_to_server(
        ChatServiceServicer(redis_client), server)

    # Listen to port 50051
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    create_grpc_connection()
