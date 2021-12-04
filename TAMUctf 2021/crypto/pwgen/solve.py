from pwn import *

a = 1103515245
c = 12345
i32_limit = 256**4//2


def generate_password():
    global seed

    pwd = []
    for _ in range(8):
        pwd.append(chr((((seed >> 16) & 0x7fff) % 0x5e) + 0x21))
        seed = ((seed * a) % i32_limit) + c

    return "".join(pwd)


if __name__ == "__main__":
    # found with find_seed.py method
    seed = 1055843420

    generate_password() # "ElxFr9)F"
    pwd = generate_password()

    io = remote("tamuctf.com", 443, ssl=True, sni="pwgen")
    io.recvline()
    io.sendline(pwd)

    flag = io.recvline()
    print(flag.decode())
