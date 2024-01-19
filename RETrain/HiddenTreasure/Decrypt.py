
Width = 0xE5
CHeight = 3
v11 = 0x839
v19 = 0x20FA
flag= [0]*0x839
f = open("./chall/inside-the-mind-of-a-hacker-memory.bmp", mode="rb")
bmpdata= f.read()

while v11 > 0:
    if CHeight < 0:
        break
    CHeight -= 1
    CWidth = Width
    Width = 0x3AA
    v19 -= 3*Width
    while v11 > 0:
        CWidth -=1
        if CWidth < 0:
            break
        v11 -=1
        a = v19 + CWidth
        dec = bmpdata[a*3 + 0x36]
        flag[v11]= dec

for i in range(0,0x838,8):
    char = (flag[i+7]<<7) + (flag[i+6]<<6) + (flag[i+5]<<5) + (flag[i+4]<<4) + (flag[i+3]<<3) + (flag[i+2]<<2) + (flag[i+1]<<1) + (flag[i]) 

    print(chr(char),end="")


        
