from protos import grpc_user_pb2_grpc, grpc_chat_pb2
from services.user_service import UserService


class UserServiceServicer(grpc_user_pb2_grpc.UserServiceServicer):
    def __init__(self, redis_client):
        self.redis_service = UserService(redis_client)

    def RegisterUser(self, register_msg_request, context):
        # Make register request and save the reply to the variable user_message
        user_message = self.redis_service.register_user(register_msg_request.username,
                                                        register_msg_request.ip, register_msg_request.port)

        print("REDIS - Register: ", user_message.message)
        return user_message

    def RemoveUser(self, request, context):
        self.redis_service.remove_user(request.username)
        return grpc_chat_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    def LookupUser(self, request, context):
        user = self.redis_service.lookup_user(request.username)
        if user.status is True:
            print(f"REDIS - Lookup: {user.username}")
        return user

    def RegisterGroup(self, register_msg_request, context):
        # Make register request and save the reply to the variable user_message
        group_message = self.redis_service.register_group(register_msg_request.group_name)

        print("REDIS - Register: ", group_message.message)
        return group_message

    def LookupGroup(self, request, context):

        group = self.redis_service.lookup_group(request.group_name)
        if group.status is True:
            print(f"REDIS - Lookup: {group.group_name}")
        return group

    def AddUserToGroup(self, request, context):
        group = self.redis_service.add_user_to_group(request.group_name)

        if group.status is True:
            print(f"REDIS - An user entered to the group chat: {group.group_name} - TOTAL: {group.num_users}")
        return group

    def DeleteUserFromGroup(self, request, context):
        group = self.redis_service.delete_user_from_group(request.group_name)

        if group.status is True:
            print(f"REDIS - An user has left the group chat: {group.group_name} - TOTAL: {group.num_users}")
        return group

