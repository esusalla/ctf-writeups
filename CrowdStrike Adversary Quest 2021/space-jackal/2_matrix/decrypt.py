import itertools


# from crypter.py, characters are encrypted / decrypted in groups of three
def C(K,M):
    B=lambda A,B,C,D,E,F,G,H,I,X,Y,Z:bytes((A*X+B*Y+C*Z&0xFF, D*X+E*Y+F*Z&0xFF,G*X+H*Y+I*Z&0xFF))
    N=len(M)
    R=N%3
    R=R and 3-R
    M=M+R*B'\0'
    return B''.join(B(*K,*W) for W in zip(*[iter(M)]*3)).rstrip(B'\0')


def crypt(a, b, c, x, y, z):
    return a*x + b*y + c*z & 0xFF


def brute_force_key(pt_group, ct_groups):
    pairs = list(zip(pt_group, ct_groups))
    for abc in POSSIBLE:
        if all(byte == crypt(*abc, *group) for byte, group in pairs):
            return abc


def crack(plaintext, ciphertext):
    pt_groups = list(zip(*[plaintext[i:i+3] for i in range(0, len(plaintext), 3)]))
    ct_groups = [ciphertext[i:i+3] for i in range(0, len(ciphertext), 3)]
    
    key = []
    for pt_group in pt_groups:
        key.append(brute_force_key(pt_group, ct_groups))
    
    return bytes([byte for group in key for byte in group])

                
if __name__ == "__main__":
    # possible bytes in key can be any value in ascii range
    POSSIBLE = list(itertools.product(range(0x80), range(0x80), range(0x80)))

    # encrypted messages
    ciphertext = bytes.fromhex("259F8D014A44C2BE8FC50A5A2C1EF0C13D7F2E0E70009CCCB4C2ED84137DB4C2EDE078807E1616C266D5A15DC6DDB60E4B7337E851E739A61EED83D2E06D618411DF61222EED83D2E06D612C8EB5294BCD4954E0855F4D71D0F06D05EE")
    # ciphertext = bytes.fromhex("259F8D014A44C2BE8F7FA3BC3656CFB3DF178DEA8313DBD33A8BAC2CD4432D663BC75139ECC6C0FFFBB38FB17F448C0817BF508074D723AAA722D4239328C6B37F57C0A5249EA4E79B780DF081E997C06058F702E2BF9F50C4EC1B5966DF27EC56149F253325CFE57A00B5749469292194F383A3535024ACA7009088E70E61289BD30B2FCFE57A00B5749469292194F383A3533BAB08CA7FD9DC778386803149280BE0895C0984C6DC77838C2085B10B3ED0040C3759B05029F8085EDBE26DE3DF25AA87CE0BBBD1169B780D1BCAA0979A6412CCBE5B68BD2FB780C5DBA34137C102DBE48D3F0AE471B77387E7FA8BEC305671785D725930C3E1D05B8BD884C0A5246EF0BF468E332E0E70009CCCB4C2ED84137DB4C2EDE078807E1616AA9A7F4055844821AB16F842")

    # plaintext appended to front of all messages
    known_plaintext = bytes("SPACEARMY", "ascii")

    # encypted known plaintext
    known_ciphertext = ciphertext[:9]
    
    key = crack(known_plaintext, known_ciphertext)

    plaintext = C(key, ciphertext)[9:]
    print(plaintext.decode())
