if __name__ == "__main__":
    with open("./writes.log") as infile:
        groups = infile.read().strip().split("\n\n")

    a = bytearray()
    b = bytearray()

    for group in groups:
        fst = bytearray()
        snd = bytearray()

        for write in group.split("\n"):
            loc, data = write.split(" ")

            try:
                data = int(data.lstrip("0x"), 16)
            except:
                print('zero')
                continue

            if loc == "0x34":
                fst.append(data)
            elif loc == "0x2C":
                snd.append(data)
            else:
                print("Unrecognized location: ", loc)
            
        print(fst.decode())
        print(snd.decode())

        a += fst
        b += snd

    print(a)
    print(b)
