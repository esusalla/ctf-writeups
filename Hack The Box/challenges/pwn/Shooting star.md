- provided with a binary that only has NX stack protections
- the binary uses `write` and `read` libc functions
- there is an overflow in the `Make a wish!` option that allows you to use the `write` function to leak addresses
- need to set `rdi` (fd), `rsi` (buf), and `rdx` (bytes) to use `write`, but `rdx` is already set to a suitable value so a ROP gadget is not needed
- after leaking addresses, server's libc can be determined to be ` libc6_2.27-3ubuntu1.4_amd64`
- can then build exploit that leaks address of `write` and uses offsets to calculate `system` and `/bin/sh` in libc in order to pop shell