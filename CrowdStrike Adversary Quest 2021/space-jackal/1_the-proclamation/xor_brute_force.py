if __name__ == "__main__":
    with open("proclamation.dat", "rb") as infile:
        barr = bytearray(infile.read())

    for key in range(0xFF):
        plain = bytearray(byte ^ key for byte in barr)
        if b"CS{" in plain:
            print(plain)
            break
