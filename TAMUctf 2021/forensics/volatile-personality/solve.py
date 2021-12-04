something = bytes.fromhex("c7ebb16296e5a9a9cb202e816cd12d0ca82a5c6e54db96d6bb5e5fad")
special = bytes.fromhex("a082d607fb9edbccaf4d4fef33b94c7ff7483d0a0bb6f3bbd42c26d0")

flag = bytearray()
for a, b in zip(something, special):
    flag.append(a ^ b)

print(flag.decode())
