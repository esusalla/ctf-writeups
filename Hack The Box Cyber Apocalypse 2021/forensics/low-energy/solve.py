from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

if __name__ == "__main__":
    with open("./key.pub") as infile:
        pub = RSA.importKey(infile.read())

    with open("./key.priv") as infile:
        priv = RSA.importKey(infile.read())

    with open("./data.hex") as infile:
        data = bytes_to_long(bytes.fromhex(infile.read()).rstrip(b"\x00"))

    msg = long_to_bytes(pow(data, priv.d, pub.n))
    print(msg)
