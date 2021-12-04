# Pwn

### TicTacToe: gigem{h3y_7h47_d035n'7_l00k_l1k3_4_p1ckl3d_54v3}
- provided with source code for Python application
- able to save state of game and reload it through unpickling
- can build a malicious class that executes "/bin/bash" when it's unpickled

### Lottery: gigem{3x3cu74bl3_rn6}
- statically linked binary without canary or PIE
- possible to overflow the name entry buffer and overwrite the return address
- name entry buffer has a consistent address, so the desired program to execute can be entered first followed by a null byte and then filler to overflow to the return address
    - not sure why buffer address is always the same or why there needs to be a two byte shift added to it so that the string starts where it should
- can construct a ROP chain that then loads EAX with 59, clears ESI, clears EDX and executes a syscall to achieve shell

### nx-oopsie: gigem{0oP5_al1_3xeCu7aB1e}
- executable stack and the program instantly gives you the value of RAX at some point then reads in name
- able to overflow buffer to get control of EIP and use the known offset of the buffer from the leaked RAX to jump to shellcode
- binary used libc.musl-x86_64.so.1 instead of glibc, so had to install to run locally
- local shellcodes worked but would not work on remote
- eventually created Alpine docker container to test on and find a shellcode that worked
- Alpine came up when searching for musl libc, so seemed the binary might have been compiled and ran on there


# Crypto

### pwgen: gigem{cryp706r4ph1c4lly_1n53cur3_prn65_DC6F9B}
- challenge says a password generation program is used to generate a group of passwords
- gives you the program and the previous password, wanting you to find the next password that would have been generated
- PRNG is self-rolled and relies on modular math and bit shifting to constantly update seed
- able to use previous password and knowledge of PRNG from source code to find potential starting seeds
- can use multiprocessing to check all possible start seeds that generate an "E" to see if they result in the target password
- once the previous password is found, the current one can be calulated by using the same seed
- submitting the current password retrieves the flag


# Sandbox

### pybox: gigem{m3m0ry_m4pp3d_f1l35}
- provided with Rust source file that shows input being ran through python in a seccomp environment
- system calls 0, 17, and 19 (read, pread64, and readv) are disabled
- possible to have Python run shellcode directly so that you can bypass the read system calls
- need to use syscall 9 (mmap) to copy file into memory after opening
- custom shellcode opens file, mmaps, then write it to stdout
- https://github.com/Apress/low-level-programming/blob/master/listings/chap4/mmap/mmap.asm
- https://defuse.ca/online-x86-assembler.htm
- https://stackoverflow.com/questions/15593214/linux-shellcode-hello-world


# Forensics

### Volatile Personality: gigem{redman_has_bad_memory}
- provided with a .lime file, indicating a Linux memory dump
- challenge name and file point towards analyzing with Volatility
- have to first find the exact kernel version in order to build a custom Volitility profile that can understand the kernel structure mappings
- running `strings mem.lime | grep -i "linux version"` gave several strings that indicated it was Ubuntu-5.4.0-42
- use QEMU to run Ubuntu and install appropriate kernel version and headers
    - `sudo apt-get linux-image-5.4.0-42-generic linux-headers-5.4.0-42-generic`
- need to restart the VM using the desired kernal
    - can change the GRUB settings in /etc/default/grub so that the GRUB boot menu appears and allows you to select the desired kernel to use, change 'GRUB_TIMEOUT_STYLE="hidden"' 'GRUB_TIMEOUT_STYLE="menu"'
	- can also set the default kernel to use in /etc/default/grub
- download Volatility and use it to create a profile in order to parse the memory dump
    - `git clone https://github.com/volatilityfoundation/volatility.git`
    - `cd volatility/tools/linux && make`
    - `zip $(lsb_release -i -s)_$(uname -r)_profile.zip ./volatility/tools/linux/module.dwarf /boot/System.map-$(uname -r)`
- place the profile into a plugins directory and load it into Volatility
    - `volatility --plugins=./<plugins directory> --info` should list available profiles (and include custom generated one)
    - `volatility --plugins=./<plugins directory> --profile==<profile name from previous command> -f <memory file> <command>`
- using the `linux_bash` command in Volatiltiy reveals that a kernel module named "somethingspecial.ko" was loaded
- checking the dmesg log with `linux_dmseg` also mentions the "somethingspecial.ko" kernel module
- possible to see all files with `linux_enumerate_files` and reveal contents of /home directory
- /home/redman/ contains folders with the "somethingspecial.ko" file, a compiled Rust binary
- possible to extract the specific file with `linux_find_file -i <inode number from linux_enumerate_files> -O <outfile>`
- reversing the retrieved kernel module reveals that at one point two sequences of bytes are xored, revealing the flag
    - kind of hard to find in complex binary, strings doesn't detect because not all bytes are printable
    - found by detecting the two symbols SOMETHING and SPECIAL in the namespaces portion of the analysis (due to how Ghidra analyzes Rust)
    - can also look for "bitxor" function in the different "namespaces" as it's a commony way to obscure a flag
    - bitxor is used on the byte sequences stored in SOMETHING and SPECIAL to reveal the flag
- https://www.andreafortuna.org/2019/08/22/how-to-generate-a-volatility-profile-for-a-linux-system/
