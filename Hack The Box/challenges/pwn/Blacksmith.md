- Takeaways:
	- seccomp can enable certain functions or disable all except a few
	- when code is executing on the stack, it's possible to use a known address of the code as a safe writable / readable area of memory
	- use `pwntools.shellcraft.execve("/bin/sh")` as a base for custom shellcode exploit writing
- provided with a binary that has full protections except there's an executable stack
- running the binary presents you with three options (`sword`, `shield`, `bow`)
- `sword` and `bow` both do nothing, but `shield` reads in input and then executes it
- at the start of the binary, a `sec` function is called that sets up a seccomp context that only allows `read` (0), `write` (1), `open` (2), and `exit` (0x3c) syscalls to be made
- possible to construct shellcode that opens `./flag.txt`, reads it, and then prints it to stdout
- trick is needing a safe place in memory to read to and then write from
- when the `shield` function reads in the input and then calls it, the address of the code is stored in `rdx`
- possible to save the value of `rdx` right at the beginning of the shellcode and then use that same area to read in the flag and then print it out

#### Tags: seccomp
