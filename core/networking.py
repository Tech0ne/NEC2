import socket

ALLOWED_CHARS_UNAME = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxy_-()[]:"

class Client:
    def __init__(self, host, port, type) -> None:
        self.host               = (host, port)
        self.username           = None
        self.public_key         = None
        self.private_key        = None
        self.remote_public_key  = None
        self.socket             = None

    def set_uname(self, username: str):
        self.username = username

    def init_connection(self):
        self.socket = socket.socket()

def setup_server():
    pass