# Binary Exploitation

## BabyArmROP
- provided with a binary that has partial RELRO, PIE, and NX stack protections (no canary)
- uses `read` to get up to 31 bytes of a name and then prints it back and says hello before reading in up to 0x200 bytes into the same buffer (exposing a buffer overflow vulnerability)
- because it uses `read` rather than `gets` or similar, a null byte is not placed at the end of the string so stack addresses after the name input can be leaked
- possible to leak an address within the binary so that the base (and gadgets) can be calculated


# Cryptography

## alice_bob_dave: zh3r0{GCD_c0m3s_70_R3sCue_3742986}
- provided with two encrypted messages and their private exponents
- also given the source code that encrypted the text, revealing that the public moduli share a factor (same p), but not given either of the public moduli
- goal is to reconstruct the public moduli for each message so that they can both be decrypted using the private exponents (e.g., pow(ct_a, d_a, n_a), missing n_a)
- due to the properties of RSA d_a * e is congruent to 1 mod n_a (same for d_b and b_a)
- multiplying d_a by e and subtracting 1 gives you a multiple of phi_a (same for d_b and phi_b)
- trial and error with smaller numbers reveals that p - 1 is a factor of the GCD of the two multiples of phi_a and phi_b
- possible to get the smaller factors of the GCD and try all combinations to reveal larger factors which you can then increase by one and test if it's prime
- if it's prime, it's likely p
- once you have p, you can use the same factor, try combos, and increase by 1 process in order to find q and r (using mult_phi_a // (p - 1) and mult_phi_b // (p - 1) for q and r, respectively)
- each test reveals there's only one possible prime for p, q, and r
- can verify that these values lead to phis that are multiples of phi_a and phi_b
- can then use p, q, and r to calculate n_a and n_b and decrypt the messages to retrieve the flag


# Web

## sparta: zh3r0{4ll_y0u_h4d_t0_d0_w4s_m0v3_th3_0bjc3ts_3mper0r}
- provided with source code for a Node.js app that uses `node-serialize` NPM package
- looking up the package reveals it's seven years old
- the GitHub repository contains several vulnerabilities including prototype pollution and RCE
- RCE exploit looks like it would do the job and can be easily confirmed locally
    - https://github.com/luin/serialize/issues/4
- server returns error messages so it's possible to use command execution to read flag and then throw that value as an error from the JavaScript

## bxss: zh3r0{{Ea5y_bx55_ri8}}
- blind XSS vulnerability on an admin feedback submission page
- sending a payload gets execute in a second or so
- poking around reveals a flag located at `/flag` (no URL ahead of endpoint)

## Baby SSRF: zh3r0{SSRF_0r_wh4t3v3r_ch4ll3ng3}
- hosted website accepts a URL, visits it, then returns the headers
- setting up a local server and having the site make a request to it reveals it's using the Python `requests` module to make its requests
- site filters out any URLs that contain "localhost", "127", "0.0.0.0", and other references to the loopback address
- possible to use URLs that resolve to "127.0.0.1" to bypass the filter and make requests to the local server (`localtest.me` resolves to "127.0.0.1")
- hint for the challenge says `for i in range(5000, 10000)`, so testing each of these ports reveals that port 9006 is hosting a service whose headers contain the flag
- https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery#bypass-using-dns-greater-than-localhost
- https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery
