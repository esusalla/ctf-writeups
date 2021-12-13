import argparse
import random
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
DEBUG = False
UNKNOWN_ERROR = 1001


def get_salt(seed=1337):  # Need a seed so the salt stays the same
    try:
        generator = random.Random(seed)
        if DEBUG:
            print(generator.getstate())
        return generator.randbytes(32)
    except:
        return UNKNOWN_ERROR


def get_token():
    try:
        generator = random.SystemRandom()
        if DEBUG:
            print(generator.getstate())
        return generator.randbytes(32)
    except:
        return UNKNOWN_ERROR


def encrypt_flag(file):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=get_salt(),
        iterations=100000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(bytes(get_token())))
    print(key)
    # Fernet uses the time and an IV so it never produces the same output twice even with the same key and data
    fernet = Fernet(key)
    return fernet.encrypt(file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt a file and save the output')
    parser.add_argument('input_file')
    parser.add_argument('output_file')

    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()
    if args.debug:
        DEBUG = True

    with open(args.input_file, "rb") as f:
        encrypted_file = encrypt_flag(f.read())

    with open(args.output_file, "wb") as f:
        f.write(encrypted_file)
