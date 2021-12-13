import json
import threading
import time

from pwn import *

start = b'{"StartGame":{"game_mode":"Easy"}}'

io = remote("54.87.142.186", 5555)
io.sendline(start)


def heartbeat():
    global io
    beat = b'{"ClientHeartBeat":{}}'

    while True:
        io.sendline(beat)
        time.sleep(1)


t = threading.Thread(target=heartbeat)
t.start()

while True:
    res = io.recvline()
    print(res)

    if b"TargetCreated" in res:
        data = json.loads(res.decode())
        x = data["TargetCreated"]["x"]
        y = data["TargetCreated"]["y"]

        payload = {"ClientClick": {"x": x, "y": y}}
        payload = json.dumps(payload).encode()
        io.sendline(payload)


