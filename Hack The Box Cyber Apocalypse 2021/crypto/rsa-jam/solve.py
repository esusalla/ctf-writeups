import ast
import math

from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse
from pwn import *

if __name__ == "__main__":
    io = remote("139.59.190.72", 31760)
    io.recvline()
    keydata = ast.literal_eval(io.recvline().decode().strip())

    key = RSA.construct((keydata["N"], keydata["e"], keydata["d"]))
    cm = math.lcm(key.p - 1, key.q - 1)
    d2 = inverse(key.e, cm)

    io.recvuntil("> ")
    io.sendline(str(d2))
    print(io.recv(1024).decode())
