BITS 64

GLOBAL write
GLOBAL read

write:
    push   rbp
    mov    rbp,rsp
    mov    DWORD [rbp-0x4],edi
    mov    QWORD [rbp-0x10],rsi
    mov    DWORD [rbp-0x8],edx
    mov    eax,0x1
    mov    edi,DWORD [rbp-0x4]
    mov    rsi,QWORD [rbp-0x10]
    mov    edx,DWORD [rbp-0x8]
    syscall
    pop    rbp
    ret

read:
    push   rbp
    mov    rbp,rsp
    mov    DWORD [rbp-0x4],edi
    mov    QWORD [rbp-0x10],rsi
    mov    DWORD [rbp-0x8],edx
    mov    eax,0x0
    mov    edi,DWORD [rbp-0x4]
    mov    rsi,QWORD [rbp-0x10]
    mov    edx,DWORD [rbp-0x8]
    syscall
    pop    rbp
    ret