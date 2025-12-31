#!/usr/bin/env python3

from pwn import *
from ctypes import *

exe = ELF("./guessMe_patched")
libc = ELF("./libc6_2.27-3ubuntu1.4_amd64.so")
ld = ELF("./ld-2.27.so")
clib = cdll.LoadLibrary("./libc6_2.27-3ubuntu1.4_amd64.so")



context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        # r = gdb.debug([exe.path],'''
        #               b* main + 122
        #               c
        #               ''')
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()

    # Get rand number
    clib.srand(clib.time(None))
    rand_num = clib.rand() % 1337
    print(hex(rand_num))
    r.sendline(f'{rand_num}'.encode())



    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
