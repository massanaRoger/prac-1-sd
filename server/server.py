from concurrent import futures
import time
import redis
import grpc

from protos import grpc_chat_pb2
from protos import grpc_chat_pb2_grpc

from services.chat_service import ChatService, chat_service


# create a class to define the server functions, derived from
# grpc_chat_pb2_grpc.ChatServiceServicer
class ChatServiceServicer(grpc_chat_pb2_grpc.ChatServiceServicer):

    def RegisterUser(self, register_msg_request, context):
        # Make register request and save the reply to the variable user_message
        user_message = chat_service.register_user(register_msg_request.chat_id, register_msg_request.username,
                                                  register_msg_request.ip, register_msg_request.port)

        print("LOG: ", user_message.message)
        return user_message


def create_grpc_connection():
    # Create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # use the generated function `add_ChatServiceServicer_to_server`
    # to add the defined class to the server
    grpc_chat_pb2_grpc.add_ChatServiceServicer_to_server(
        ChatServiceServicer(), server)

    # Listen to port 50051
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    server.wait_for_termination()

    # try:
    #     while True:
    #         time.sleep(86400)
    # except KeyboardInterrupt:
    #     server.stop(0)


if __name__ == "__main__":
    create_grpc_connection()
