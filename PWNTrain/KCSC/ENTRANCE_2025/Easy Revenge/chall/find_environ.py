#!/usr/bin/python3
from pwn import *


libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')


environ_addr = libc.symbols['environ']
log.success(f"Libc Environ Address: {hex(environ_addr)}")


