- provided with a binary with an obvious buffer overflow resulting from `fgets`
- the only gadget needed to complete the ROP is `pop rdi; ret`
- don't know libc version being used on the server, so first have to leak addresses and fingerprint libc
	- had trouble getting reliable results from blukat
	- ended up having to try different combinations of leaks and fuzzing the "/bin/sh" string address
- after libc is fingerprinted, it's possible to build a payload that opens a shell on the server
