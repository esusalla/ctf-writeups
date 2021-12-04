from pwn import *

if __name__ == "__main__":
    io = remote("188.166.145.178", 31335)
    io.recvuntil("> ")
    io.sendline("1")

    res = io.recvuntil("\n> ")
    key = res.decode().split("\n")[2].split(" -> ")
    key = [pair.split(" ") for pair in key]
    syms = {key[0][0]: key[1][0]}
    for i, k in enumerate(key[1:-1]):
        syms[k[1]] = key[i+2][0]

    io.sendline("2")

    i = 1
    while i <= 500:
        print(i)
        res = io.recvuntil("Answer: ")
        question = res.decode().split("\n")[-3].rstrip("= ?")
        question = "".join(syms[c] if c in syms else c for c in question)
        answer = eval(question)
        io.sendline(str(answer))
        i += 1

    io.interactive()
