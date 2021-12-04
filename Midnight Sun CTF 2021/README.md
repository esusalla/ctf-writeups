# Web

### gurkburk: midnight{d311c10u5_p1ck135_f0r_3v3ry0n3}
- program allows you to save information and then reload it using pickling
- possible to modify saved pickle so that it executes open and read functions to retrieve flag

### Corporate MFA: midnight{395E160F-4DB8-4D7A-99EF-08E6799741B5}
- website unserializes user provided data, but can't take advantage of any "magic" PHP functions
- use array and object reference to link "mfa" with "_correctValue" and bypass authentication check


# Crypto

### Backup - alice: midnight{factorization_for_the_Win}
- two public keys provided
- extracting N from each and using GCD allows you to retrieve p
- once p is retrieved, you can find q, phi, d, and reconstruct private key
- use private key to SSH into server and retrieve flag
    - use `ssh-keygen -f key.pub -e -m pem` to convert public key from authorized_keys into PEM format

### Backup - bob: midnight{Turn_electricity_t0_h347}
- RsaCtfTool reveals that the extracted public key is vulnerable to the smallq attack, allowing retrieval of the private key

### Backup - frank: midnight{D0_n07_s0w_p4r75_0f_y0ur_pr1v473}
- q can be recovered from portion of visible private key, allowing d and full private key to be recovered
- https://blog.cryptohack.org/twitter-secrets
