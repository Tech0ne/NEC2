###############################################
#   ___                       _   _          
#  | __|_ _  __ _ _ _  _ _ __| |_(_)___ _ _  
#  | _|| ' \/ _| '_| || | '_ \  _| / _ \ ' \ 
#  |___|_||_\__|_|  \_, | .__/\__|_\___/_||_|
#                   |__/|_|                  
#
###############################################

from .imports import *


###################
##
## RsaKeys
##
###################

class RsaKeys:
    def __init__(self, length: int = 2048, public_key: rsa.PublicKey = None, private_key: rsa.PrivateKey = None):
        self.public_key = public_key
        self.private_key = private_key
        self.length = length
    
    def export_certificate(self):
        key = save_key(self.public_key)
        key = [key.decode()[i:i+50] for i in range(0, len(key), 50)]
        key = '\n'.join(key)
        certif = f"""----- START NEC2 PUBLIC KEY -----
{key}
----- FINISH NEC2 PUBLIC KEY -----"""

    def import_certificate(self, certif: bytes):
        if ((not b"----- START NEC2 PUBLIC KEY -----\n" in certif) or
            (not b"\n----- FINISH NEC2 PUBLIC KEY -----" in certif)):
           raise ValueError("Invalid certificate format")
        key = certif.split('-\n')[1].split('\n-')[0]
        key = key.replace('\n', '')
        self.public_key = load_key(key, rsa.PublicKey)
        return self

def save_key(key: rsa.PublicKey | rsa.PrivateKey) -> bytes:
    return base64.b64encode(key.save_pkcs1("PEM"))

def load_key(key: bytes, key_type_priv: bool = False) -> rsa.PublicKey | rsa.PrivateKey:
    key_type = rsa.PrivateKey if key_type_priv else rsa.PublicKey
    return key_type.load_pkcs1(base64.b64decode(key))

def generate_rsa_keys(length: int) -> RsaKeys:
    if length < 90:
        raise ValueError("\"length\" is too short to have a working RSA system")
    (pub, pri) = rsa.newkeys(length)
    return RsaKeys(length, pub, pri)

def sign(message: bytes, private_key: rsa.PrivateKey) -> bytes:
    return rsa.sign(message, private_key, "SHA-256")

def verify(message: bytes, signature: bytes, public_key: rsa.PublicKey) -> bool:
    try:
        return rsa.verify(message, signature, public_key) == "SHA-256"
    except:
        return False

def encrypt(data: bytes, extern_public_key: rsa.PublicKey, intern_private_key: rsa.PrivateKey) -> bytes:
    chunk_size = rsa.common.byte_size(extern_public_key.n) - 11
    splitted_message = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    encrypted_message = [base64.b64encode(rsa.encrypt(chunk, extern_public_key)) for chunk in splitted_message]
    final_message = b';'.join(encrypted_message)
    signature = sign(final_message, intern_private_key)
    joined_message = final_message + b'|' + base64.b64encode(signature)
    return joined_message

def decrypt(data: bytes, intern_private_key: rsa.PrivateKey, extern_public_key: rsa.PublicKey) -> bytes:
    pipe_count = data.count(b'|')
    if pipe_count != 1:
        raise ValueError(f"Invalid formating : expecting 1 '|' but found {pipe_count}")
    message, signature = data.split(b'|')
    if not verify(message, base64.b64decode(signature), extern_public_key):
        raise ValueError("Could not verify signature of message")
    chunk_size = rsa.common.byte_size(intern_private_key.n) - 11
    decrypted_message = [rsa.decrypt(base64.b64decode(chunk), intern_private_key) for chunk in message.split(b';')]
    if any([len(chunk) != chunk_size for chunk in decrypted_message[:-1]]):
        raise ValueError("Invalid chunk size !")
    return b''.join(decrypted_message)