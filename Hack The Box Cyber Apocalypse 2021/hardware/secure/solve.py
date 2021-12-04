if __name__ == "__main__":
    with open("./data") as infile:
        data = infile.read().strip().split(" ")

    msg = bytearray()
    for pair in data:
        fst, snd = pair.split("/")
        if fst == "0x00" or fst == "0xFF" or snd == "0x00":
            continue
        
        try:
            msg.append(int(fst.lstrip("0x"), 16))
        except:
            print(fst, snd)

    print(msg)
