import base64
import codecs
import urllib

from pwn import *

# connect
io = remote("pwn-2021.duc.tf", 31905)
io.recv()
io.sendline()

# math
io.recv()
io.sendline(b"2")

# parse hex number
num = io.recv().decode().split(" ")[-1].strip()
num = str(int(num, 0)).encode()
io.sendline(num)

# convert to ASCII
num = io.recv().decode().split(" ")[-1].strip()
char = chr(int(num, 16)).encode()
io.sendline(char)

# parse URL encoded string
msg = io.recv().decode().split(" ")[-1].strip()
msg = urllib.parse.unquote(msg).encode()
io.sendline(msg)

# decode base64
msg = io.recv().decode().split(" ")[-1].strip()
msg = base64.b64decode(msg)
io.sendline(msg)

# encode base64
msg = io.recv().decode().split(" ")[-1].strip()
msg = base64.b64encode(msg.encode())
io.sendline(msg)

# encode rot13
msg = io.recv().decode().split(" ")[-1].strip()
msg = codecs.encode(msg, 'rot_13').encode()
io.sendline(msg)

# decode rot13
msg = io.recv().decode().split(" ")[-1].strip()
msg = codecs.decode(msg, 'rot_13').encode()
io.sendline(msg)

# parse binary number
num = io.recv().decode().split(" ")[-1].strip()
num = str(int(num, 2)).encode()
io.sendline(num)

# encode binary number
num = io.recv().decode().split(" ")[-1].strip()
num = bin(int(num)).encode()
io.sendline(num)

io.recv()
io.sendline(b"DUCTF")
print(io.recv())
