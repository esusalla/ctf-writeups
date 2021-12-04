import subprocess

if __name__ == "__main__":
    with open("./out.txt") as infile:
        enc = bytes.fromhex(infile.read())

    seed = 1618572736
    
    while True:
        print(seed)
        proc = subprocess.run(["./crabber/target/debug/crabber", str(seed)], capture_output=True)
        xor = [int(n) for n in proc.stdout.decode().split(" ") if n]

        flag = bytearray(a ^ b for a, b in zip(enc, xor))
        if b"CHTB{" in flag:
            print(flag.decode())
            print(seed)
            break 
        seed -= 1

