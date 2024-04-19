import json

from client.discovery import Discovery
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
        if redis_message is None:
            return grpc_user_pb2.LookupUserReply(status=False, username="", ip="", port=-1)
        else:
            parsed_message = json.loads(redis_message)
            return grpc_user_pb2.LookupUserReply(status=True, username=user_to_chat, ip=parsed_message["ip"],
                                                 port=parsed_message["port"])

    def register_group(self, group_name: str):

        self.redis_client.set(group_name, 1)
        discovery_server = Discovery(group_name, is_group=True)
        discovery_server.receive_thread.start()
        return grpc_user_pb2.RegisterMessageReply(message=f"The group '{group_name}'"
                                                          f"has been registered to Redis!")

    def lookup_group(self, group_name):
        num_users = self.redis_client.get(group_name)
        if num_users is None:
            return grpc_user_pb2.LookupGroupReply(status=False, group_name=group_name, num_users=0)

        else:
            return grpc_user_pb2.LookupGroupReply(status=True, group_name=group_name, num_users=int(num_users))

    def add_user_to_group(self, group_name):
        group_details = self.lookup_group(group_name)
        if group_details.num_users != 0:
            new_num_users = group_details.num_users + 1
            self.redis_client.set(group_name, new_num_users)
            return grpc_user_pb2.LookupGroupReply(status=False, group_name=group_name, num_users=new_num_users)
        return grpc_user_pb2.LookupGroupReply(status=False, group_name=group_name, num_users=0)

    def delete_user_from_group(self, group_name):
        group_details = self.lookup_group(group_name)
        if group_details.num_users != 0:
            new_num_users = group_details.num_users - 1
            self.redis_client.set(group_name, new_num_users)
            return grpc_user_pb2.LookupGroupReply(status=False, group_name=group_name, num_users=new_num_users)
        return grpc_user_pb2.LookupGroupReply(status=False, group_name=group_name, num_users=0)
