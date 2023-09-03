import base64

import rsa

def save_key(key: rsa.PublicKey | rsa.PrivateKey) -> bytes:
    return base64.b64encode(key.save_pkcs1("PEM"))

def load_key(key: bytes, key_type: rsa.PublicKey | rsa.PrivateKey) -> rsa.PublicKey | rsa.PrivateKey:
    return key_type.load_pkcs1(base64.b64decode(key))

def generate_rsa_keys(length: int) -> (rsa.PublicKey, rsa.PrivateKey):
    if length < 90:
        raise ValueError("\"length\" is too short to have a working RSA system")
    return rsa.newkeys(length)

def encrypt(data: bytes, public_key: rsa.PublicKey) -> bytes:
    chunk_size = rsa.common.byte_size(public_key.n) - 11
    splitted_message = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    encrypted_message = [base64.b64encode(rsa.encrypt(chunk, public_key)) for chunk in splitted_message]
    return b';'.join(encrypted_message)

def decrypt(data: bytes, private_key: rsa.PrivateKey) -> bytes:
    if data == b"":
        return b""
    chunk_size = rsa.common.byte_size(private_key.n) - 11
    splitted_message = data.split(b';')
    if any(len(chunk) != chunk_size for chunk in splitted_message[:-1]):
        raise ValueError("Invalid chunk size !")
    return b''.join([rsa.decrypt(base64.b64decode(chunk), private_key) for chunk in splitted_message])