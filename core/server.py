################################
#   ___                      
#  / __| ___ _ ___ _____ _ _ 
#  \__ \/ -_) '_\ V / -_) '_|
#  |___/\___|_|  \_/\___|_|  
#                            
################################

from .connections import Connection
from .encryptions import RsaKeys
from .imports import *
from .utils import *

class Server:
    def __init__(self, host: str, port: int, keys: RsaKeys, use_ngrok: bool = False, ngrok_auth_token: str = None) -> None:
        self.host = host
        self.port = port
        self.rhost = self.host
        self.rport = self.port
        self.keys = keys
        self.use_ngrok = use_ngrok
        self.tunnel = None
        if self.use_ngrok:
            if ngrok_auth_token is None:
                raise ValueError("ngrok need auth token !")
            from .ngrok_integration import forward_port, kill_all_ngrok_tunnels
            try:
                self.rhost, self.rport, self.tunnel = forward_port(self.port, ngrok_auth_token)
            except:
                kill_all_ngrok_tunnels()
                self.rhost, self.rport, self.tunnel = forward_port(self.port, ngrok_auth_token)
        self.access_url = self.rhost + ':' + str(self.rport)

class RemoteClient:
    pass