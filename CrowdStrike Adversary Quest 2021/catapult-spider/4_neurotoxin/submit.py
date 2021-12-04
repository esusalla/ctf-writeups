import pwn
import time

if __name__ == "__main__":
    with open("./forged-pictures/forged1.dat") as infile:
        forged_1 = infile.read()

    with open("./forged-pictures/forged2.dat") as infile:
        forged_2 = infile.read()

    with open("./forged-pictures/forged3.dat") as infile:
        forged_3 = infile.read()

    # Connect
    conn = pwn.remote("neurotoxin.challenges.adversary.zone", 40755)
    time.sleep(1)
    res = conn.recv().decode()
    print(res)

    # Send first forged picture
    time.sleep(1)
    conn.sendline(forged_1)
    time.sleep(1)
    res = conn.recv().decode()
    print(res)

    # Send second forged picture
    time.sleep(1)
    conn.sendline(forged_2)
    time.sleep(1)
    res = conn.recv().decode()
    print(res)

    # Send third forged picture
    time.sleep(1)
    conn.sendline(forged_3)
    time.sleep(1)
    res = conn.recvall().decode()

    # Write serialized flag image from respone to file
    flag = res.strip().split("\n")[-1].split(" ")[-1]
    with open("flag.dat", "w") as outfile:
        outfile.write(flag)

