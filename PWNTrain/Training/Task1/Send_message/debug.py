#!/usr/bin/python3

from pwn import *

p = gdb.debug("./sendmsg")
#p = process("./sendmsg")
p.interactive()