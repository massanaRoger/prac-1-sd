class PrivateChatException(Exception):
    """The private chat is already full"""

    def __init__(self, message="An error occurred in the private chat"):
        self.message = message
        super().__init__(self.message)