import string

mapping = {}

for value in string.printable.encode():
    key = 13*value**2 + 3*value + 7
    mapping[key] = value

with open("./output.txt") as infile:
    encrypted = infile.read().strip()
    flag = "".join(chr(mapping[ord(c)]) for c in encrypted)

print(flag)
