import os


class Configuration:
    def __init__(self):
        self.connection_string = os.environ["DATABASE_CONNECTION_STRING"]
        self.redis_connection_string = os.environ["REDIS_CONNECTION_STRING"]
