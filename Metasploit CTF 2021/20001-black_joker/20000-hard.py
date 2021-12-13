import json
import threading
import time

from pwn import *
from Crypto.Util.number import bytes_to_long

start = bytes.fromhex("00000020000000000000000c00020001000000030000000c00024e8400000003")

io = remote("54.87.142.186", 5555)
io.send(start)


def heartbeat():
    global io
    beat = bytes.fromhex("00000014000000000000000c0002000100000001")

    while True:
        io.send(beat)
        time.sleep(1)


t = threading.Thread(target=heartbeat)
t.start()

while True:
    size = bytes_to_long(io.recvn(4))

    if size == 0x38:
        # new target
        data = io.recvn(size - 4)
        x = data[36:40].hex()
        y = data[48:].hex()
        click = "0000002c000000000000000c00020001000000070000000c00024ee8" + x + "0000000c00024ee9" + y
        click = bytes.fromhex(click)
        io.send(click)
        print("[-] NEW TARGET")

    elif size == 0x44:
        # hit target
        data = io.recvn(size - 4)
        print("[+] HIT!")

    elif size == 0x2c:
        # missed target
        io.recvn(size - 4)
        print("[-] MISS")
    
    else:
        print(io.recvall())
