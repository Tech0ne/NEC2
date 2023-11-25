####################################
#   ___         _               _ 
#  | _ \_ _ ___| |_ ___  __ ___| |
#  |  _/ '_/ _ \  _/ _ \/ _/ _ \ |
#  |_| |_| \___/\__\___/\__\___/_|
#
####################################

from .imports import *
from .globals import *

class Message:
    def __init__(self, method: bytes = PING, arguments: list[bytes] = [], origin = SERVER) -> None:
        self.method = method
        self.arguments = arguments
        self.origin = origin

        if origin == SERVER and not method in SERVER_SIDE_PROTOCOL_METHODS:
            raise ValueError("Method is not part of server initiated requests")
        if origin == CLIENT and not method in CLIENT_SIDE_PROTOCOL_METHODS:
            raise ValueError("Method is not part of client initiated requests")
    
    def build_message(self) -> bytes:
        final_message = self.method

        final_message += b':'
        final_message += b':'.join([base64.b64encode(argument) for argument in self.arguments])

        return final_message
    
    def load_message(self, message: bytes, origin = SERVER):
        self.method = message.split(b':')[0]
        self.origin = origin

        self.arguments = [base64.b64decode(argument) for argument in message.split(b':')[1:]]

        if origin == SERVER and not self.method in SERVER_SIDE_PROTOCOL_METHODS:
            raise ValueError("Method is not part of server initiated requests")
        if origin == CLIENT and not self.method in CLIENT_SIDE_PROTOCOL_METHODS:
            raise ValueError("Method is not part of client initiated requests")