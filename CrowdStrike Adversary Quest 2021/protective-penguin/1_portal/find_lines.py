if __name__ == "__main__":
    # "/lib64/ld-linux-x86-64.so.2" string can be found in binary
    # possible to overwrite address of filename that is opened and searched for user:pass
    with open("/lib64/ld-linux-x86-64.so.2", "rb") as infile:
        ba = bytearray(infile.read())

    count = 0
    found = False
    line = bytearray()
    ln = 0

    for byte in ba:
        if count < 256:
            if byte == ord("\n"):
                if found:
                    print(f"{ln}, {len(line)}: {bytes(line)}")

                # Reset for new line
                count = 0
                found = False
                line = bytearray()
                ln += 1
            else:
                count += 1
                # Look for lines containing ":"
                if byte == ord(":"):
                    found = True
                line.append(byte)
        else:
            if found:
                print(f"{ln}, {len(line)}: {bytes(line)}")

            # Reset for new line
            count = 0
            found = False
            line = bytearray()
            ln += 1

    if found:
        print(f"{ln}, {len(line)}: {bytes(line)}")
