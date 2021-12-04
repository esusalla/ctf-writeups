if __name__ == "__main__":
    with open("./key_presses.csv") as infile:
        lines = infile.readlines()[1:]
        codes = [line.split(",")[6].strip('"') for line in lines]

    with open("./key_presses.hex", "w") as outfile:
        outfile.write("\n".join(codes))
