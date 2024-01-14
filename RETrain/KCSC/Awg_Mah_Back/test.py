from pwn import *
with open('flag.txt', 'rb') as (f):
    flag = f.read()

a = flag[0:len(flag) // 3]
b = flag[len(flag) // 3:2 * len(flag) // 3]
c = flag[2 * len(flag) // 3:]

c = xor(c, int(str(len(flag))[0]) * int(str(len(flag))[1]))
c = xor(b, c)
b = xor(a, b)
a = xor(c, a)
c = xor(b, c)
b = xor(a, b)
a = xor(a, int(str(len(flag))[0]) + int(str(len(flag))[1]))

dcr = a + b + c
print(chr(dcr))