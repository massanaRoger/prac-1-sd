import json

from protos import grpc_user_pb2


class UserService:

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def register_user(self, username: str, ip: str, port: int):
        address = {
            "ip": ip,
            "port": port
        }

        self.redis_client.set(username, json.dumps(address))
        return grpc_user_pb2.RegisterMessageReply(message=f"The user '{username}' with IP: '{ip}' and PORT: '{port}' "
                                                          f"has been registered to Redis!")

    def lookup_user(self, user_to_chat):
        redis_message = self.redis_client.get(user_to_chat)
        print(redis_message)
        if redis_message is None:
            return grpc_user_pb2.LookupUserReply(status=False, username="", ip="", port=-1)
        else:
            parsed_message = json.loads(redis_message)
            return grpc_user_pb2.LookupUserReply(status=True, username=user_to_chat, ip=parsed_message["ip"],
                                                 port=parsed_message["port"])
