#!/usr/bin/env python3
                                              #Format Flag: ictf{}
def enc(b):
 a = [n for n in range(b[0]*2**24+b[1]*2**16+b[2]*2**8+b[3]+1)][1:] # [1:] cat mang lay tu phan tu thu 1
# (b[0]*2**24+b[1]*2**16+b[2]*2**8+b[3]+1) ghep cac byte lai voi nhau
# *2 = <<1

 c,i = 0,0
 while len([n for n in a if n != 0]) > 1: #len([n for n in a if n != 0]) : lay kich thuoc cua mang(khong tinh phan tu = 0)
  
  i%=len(a)
  if (a[i]!=0 and c==1):
   a[i],c=0,0 # a[i] = c = 0
  if (a[i] != 0):
   c+=1
  i += 1
 return sum(a)

print(r"""
    .----.   @   @
   / .-"-.`.  \v/
   | | '\ \ \_/ )
 ,-\ `-.' /.'  /
'---`----'----'
""")
flag = input("Enter flag here: ").encode() #encode UTF-8

out = b'' #b'' : empty byte string
for n in [flag[i:i+4] for i in range(0,len(flag),4)]: #flag[i:i+4] cat mang tu i den i+4
  #(0,len(flag),4) i chay tu 0 -> len(flag) khoang cach giua cac vong la 4
  out += bytes.fromhex(hex(enc(n[::-1]))[2:].zfill(8)) #n[::-1] dao nguoc mang n
#hex(enc(n[::-1])) chuyen phan tu mang thanh dang hex
if out == b'L\xe8\xc6\xd2 f\xde\xd4\xf6 j\xd0\xe0\xca d\xe0\xbe\xe6 J\xd8\xc4\xde `\xe6\xbe\xda >\xc8\xca\xca ^\xde\xde\xc4 ^\xde\xde\xdez\xe8\xe6\xde':
# 4ce8c6d2 66ded4f6 6ad0e0ca 64e0bee6 4ad8c4de 60e6beda 3ec8caca 5ededec4 5ededede 7ae8e6de
 print("[*] Flag correct!")
else:
 print("[*] Flag incorrect.")
 #641707941791103776372199586313957493399609603586927934429390687588239378448484341645145350399710
