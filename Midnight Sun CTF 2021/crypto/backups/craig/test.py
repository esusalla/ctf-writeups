outfile = open("hex.txt", "a")
with open("/usr/share/wordlists/rockyou.txt", "r", encoding="ISO-8859-1") as infile:
    lines = infile.readlines()
    for line in lines:
        line = line.strip()
        if line:
            outfile.write(line.encode().hex() + "\n")
