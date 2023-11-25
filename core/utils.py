#############################
#   _   _ _   _ _    
#  | | | | |_(_) |___
#  | |_| |  _| | (_-<
#   \___/ \__|_|_/__/
#                    
#############################

from .imports import *

def networksafe(data: bytes, is_rsa: bool = True):
    if is_rsa:
        return b'<RSA:' + data + b'>\n'
    return b'<RAW:' + base64.b64encode(data) + b'>\n'