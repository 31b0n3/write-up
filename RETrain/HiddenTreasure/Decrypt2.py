from pwn import *

f = open("inside-the-mind-of-a-hacker-memory.bmp", "rb")
data=f.read()
binaryString=""
StartOfImage = u32(data[10:14])
data = data[StartOfImage:]
j=0
for i in range(256):
    binaryString += str(data[3*j])
    j+=1
print(binaryString)
flag=""
for i in range(0,len(binaryString),8):
    try:
        flag += chr(int("".join(reversed(binaryString[i:i+8])),2))
    except:
        break
print(flag)