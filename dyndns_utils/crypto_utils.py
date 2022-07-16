#!/usr/bin/env python3

from genericpath import isdir
import sys
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def get_encrypted_message(public_key, msg):
    encrypted = public_key.encrypt(
        msg.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted


def get_decrypted_message(crypt_msg, private_key):
    msg = private_key.decrypt(crypt_msg,
                                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                            algorithm=hashes.SHA256(),
                                            label=None
                                            )
                                )
    return msg.decode()


def read_private_key(filename, password):
    private_key  = None
    with open(filename, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(),
                                                            password=password,
                                                            backend=default_backend()
                                                            )
    return private_key


def read_public_key(filename):
    public_key  = None
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(),
                                                        backend=default_backend()
                                                        )
    return public_key


def store_public_key(public_key, filename):
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                                    )

    with open(filename, 'wb') as f:
        f.write(pem)


def store_private_key(private_key, filename):
    pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PrivateFormat.PKCS8,
                                    encryption_algorithm=serialization.NoEncryption()
                                    )

    with open(filename, 'wb') as f:
        f.write(pem)


def create_key(size, exponent):
    private_key = rsa.generate_private_key(public_exponent=exponent,
                                            key_size=size,
                                            backend=default_backend()
                                            )

    public_key = private_key.public_key()

    return (private_key, public_key)


if (__name__ == '__main__'):
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        root_dir = sys.argv[1]
    else:
        root_dir = os.path.dirname(__file__)

    private_key, public_key = create_key(4096, 65537)
    store_private_key(private_key, os.path.join(root_dir, 'private_key.pem'))
    store_public_key(public_key, os.path.join(root_dir, 'public_key.pem'))