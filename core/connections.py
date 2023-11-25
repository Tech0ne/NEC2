####################################################
##    ___                      _   _             
##   / __|___ _ _  _ _  ___ __| |_(_)___ _ _  ___
##  | (__/ _ \ ' \| ' \/ -_) _|  _| / _ \ ' \(_-<
##   \___\___/_||_|_||_\___\__|\__|_\___/_||_/__/
##                                               
####################################################

from .encryptions import *
from .imports import *
from .utils import *

class Connection:
    def __init__(self, host: str, port: int, raw_connection: socket.socket, keys: RsaKeys = None, remote_pub_key: RsaKeys = None) -> None:
        self.host = host
        self.port = port
        self.socket = raw_connection
        self.keys = keys
        self.remote_pub_key = remote_pub_key
        self.use_rsa = False
        self.update_rsa()

        self.data_save = b""

    def send_data(self, data: bytes):
        if self.use_rsa:
            self.socket.send(networksafe(encrypt(data, self.remote_pub_key.public_key, self.keys.private_key)))
        else:
            self.socket.send(networksafe(data, False))
    
    def receive_data(self) -> bytes:
        if self.data_save == b"":
            self.data_save = self.socket.recv(4096)
        
        if not len(self.data_save):
            raise ValueError("Empty buffer received")

        if chr(self.data_save[0]).encode() != b'<':
            raise ValueError(f"Invalid data : should be starting with a b'<' but starts with b'{chr(self.data_save[0])}'")
        
        nb_empty = 0

        while (not b'>' in self.data_save) or (chr(self.data_save[-1]) == '>'):
            recv = self.socket.recv(4096)
            if not recv:
                nb_empty += 1
            if nb_empty >= 10:
                raise ValueError("Empty buffer received")
            self.data_save += recv
        
        if not b'\n' in self.data_save:
            self.data_save = self.data_save.replace(b'>', b'>\n')
        
        data = self.data_save.split(b'<')[1].split(b'>')[0]
        self.data_save = b'\n'.join(self.data_save.split(b'\n')[1:])

        if len(data) <= 4:
            raise ValueError("Empty buffer received")
        
        if (not data.startswith(b"RAW:")) and (not data.startswith(b"RSA:")):
            raise ValueError(f"Invalid received data : starting with : {data[:4]}")
        
        if data.startswith(b"RSA:") and self.keys is None:
            raise ValueError("RSA asked, but currently not activated")
        
        if data.startswith(b"RSA:"):
            return decrypt(data[4:], self.keys.private_key, self.remote_pub_key.public_key)
        return base64.b64decode(data[4:])

    def set_keys(self, rsa_keys: RsaKeys):
        self.keys = rsa_keys
    
    def set_remote_certificate(self, remote_pub_key: RsaKeys):
        self.remote_pub_key = remote_pub_key
    
    def update_rsa(self):
        self.use_rsa = (self.keys is not None and
                        self.keys.public_key is not None and
                        self.keys.private_key is not None and
                        self.remote_pub_key is not None and
                        self.remote_pub_key.public_key is not None and
                        self.remote_pub_key.private_key is None)