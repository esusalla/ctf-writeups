if __name__ == "__main__":
    with open("./icmp.hex") as infile:
        lines = infile.readlines()
    
    i = 0
    limit = len(lines) - 1
    data = []

    while i < limit:
        data.append(lines[i][16:48])
        if lines[i] == lines[i+1]:
            i += 2
        else:
            i += 1
            
    with open("fini.zip", "wb") as outfile:
        outfile.write(bytes.fromhex("".join(data)))

