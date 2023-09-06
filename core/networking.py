from .encryptions import *

import json
import socket
import threading

ALLOWED_CHARS_UNAME = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxy_-()[]:"

class Client:
    def __init__(self, host: str, port: int, key_length: 2048) -> None:
        self.host               = (host, port)
        self.key_length         = key_length
        self.stop_event         = threading.Event()
        self.messages           = []
        self.customisation      = {
            # Remote configs
            "border_style": "red",
            "uname_style": "yellow",
            "footer": None,
            "footer_style": "",
            # Local configs
            "signature": ""
        }
        self.self_password      = ""
        self.is_rsa_enabled_yet = False
        self.remote_passwd      = None
        self.username           = None
        self.public_key         = None
        self.private_key        = None
        self.remote_public_key  = None
        self.socket             = None
        self.recv_thread        = None
        self.is_running         = None

    def init_connection(self):
        self.socket = socket.socket()
        self.socket.connect(self.host)
        self.send_srv(b"PING")
        if self.recv(128) != b"PONG":
            raise ConnectionError("Server did not respond correctly")
        self.public_key, self.private_key = generate_rsa_keys(self.key_length)
        pub_key = base64.b64encode(save_key(self.public_key)).decode()
        self.send_srv(f"PUBKEY {pub_key}".encode())
        response = self.recv_srv(4096)
        if not response.startswith(b"PUBKEY "):
            raise ConnectionError("Server did not respond correctly")
        self.set_remote_rsa(response[7:])
    
    def set_customisation(self, new_customisation: dict):
        for k, v in new_customisation.items():
            if not k in self.customisation:
                raise ValueError(f"Key \"{k}\" is not a valid customisation !")
            self.customisation[k] = v
    
    def set_remote_rsa(self, rsa_key: bytes):
        self.remote_public_key = load_key(rsa_key, rsa.PublicKey)
        self.is_rsa_enabled_yet = True

    def send_encrypted(self, data: bytes):
        if not self.socket:
            raise ConnectionError("Client not connected")
        if not self.is_rsa_enabled_yet:
            raise ValueError("Remote Public RSA Key not set")
        self.socket.send(encrypt(data, self.remote_public_key))

    def send_srv(self, data: bytes):
        if not self.socket:
            raise ConnectionError("Client not connected")
        if self.is_rsa_enabled_yet:
            self.send_encrypted(data)
        else:
            self.socket.send(data)

    def recv_encrypted(self, size: int) -> bytes:
        if not self.socket:
            raise ConnectionError("Client not connected")
        if not self.is_rsa_enabled_yet:
            raise ValueError("Private RSA Key not set")
        return decrypt(self.socket.recv(size), self.private_key)
    
    def recv_srv(self, size: int) -> bytes:
        if not self.socket:
            raise ConnectionError("Client not connected")
        if self.is_rsa_enabled_yet:
            return self.recv_encrypted(size)
        else:
            return self.socket.recv(size)

class Server:
    def __init__(self, host, port) -> None:
        self.host               = (host, port)
        self.socket             = None
        self.clients            = {}
    
    def add_client(self, connection: socket.socket, public_key: rsa.PublicKey, uname: str, customisation: dict) -> typing.Tuple(bool, str):
        if uname in self.clients.keys():
            return (False, "Username exists")