import math

from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse

if __name__ == "__main__":
    with open("work.pub") as infile:
        key_work = RSA.importKey(infile.read())
    with open("home.pub") as infile:
        key_home = RSA.importKey(infile.read())

    p = math.gcd(key_work.n, key_home.n)
    q = key_work.n // p
    phi = (p-1) * (q-1)
    d = inverse(key_work.e, phi)

    key_priv = RSA.construct((key_work.n, key_work.e, d))
    with open("alice.priv", "wb") as outfile:
        outfile.write(key_priv.exportKey())
