from pwn import *

with open('flag.txt', 'rb') as (f):
    flag = f.read()
a = flag[0:len(flag) // 3]
b = flag[len(flag) // 3:2 * len(flag) // 3]
c = flag[2 * len(flag) // 3:]
a = xor(a, int(str(len(flag))[0]) + int(str(len(flag))[1]))
b = xor(a, b)
c = xor(b, c)
a = xor(c, a)
b = xor(a, b)
c = xor(b, c)
c = xor(c, int(str(len(flag))[0]) * int(str(len(flag))[1]))
enc = a + b + c
with open('output.txt', 'wb') as (f):
    f.write(enc)


# 00 00 41 39 2C 74 1F 45 34 2B 36 26 01 03 3A 47 37 12 00 39 0F 10 2E 12 05 2D 63 0E 01 5D 36 48 35 75 1F 6F 32 3D 67 69 00 36 03 2E 1A 74 0B 30 32 1D 3D 08 04 3A 25 60 02 3C 2A 45 0E 02 31 35 04 04 7C 09 1C 38 3E 00 02 00 77 55 06 39 0F 77 57 6F 33 55 63 30 4F 33 55 6F 7A 45 61 54 54 76 61 45 6A 4C 54 45 7A 63 54 44 54 6D 51 33 6D 7A 63 46 58 54 60 6E 58 56
#120