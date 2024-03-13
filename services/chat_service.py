import json

import redis

from protos import grpc_chat_pb2_grpc
from protos import grpc_chat_pb2


class ChatService:

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def register_user(self, chat_id: str, username: str, ip: str, port: int):

        message = {
            "username": username,
            "ip": ip,
            "port": port
        }

        self.redis_client.set(chat_id, json.dumps(message))
        return grpc_chat_pb2.RegisterMessageReply(message=f"Chat ID: '{chat_id}' has the user: '{username}' "
                                                          f"registered with '{ip}' and '{port}'!")

    # def LookupUser(self, request, context):
    #     username = request.username
    #     result = self.redis_client.get(username)
    #     if result:
    #         address = result.decode('utf-8')
    #         return grpc_chat_pb2.LookupUserReply(status="FOUND", username=username, address=address)
    #     else:
    #         return grpc_chat_pb2.LookupUserReply(status="NOT FOUND", username=username, address="")


redis_client = redis.Redis(host='localhost', port=6379, db=0)
chat_service = ChatService(redis_client)
