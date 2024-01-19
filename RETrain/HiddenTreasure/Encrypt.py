Width = 0x3AA
Height = 0x244
v11 = 0x838
count1 = 0
v19 = 0
CWidth = 0
addr = [1]* 0x839
bmp = [0]*100000
Cheight = 0
while count1 <= v11:
    if Cheight >= Height:
        break
    CWidth = 0
    while count1 <= v11:
        if CWidth >= Width:
            break
        if count1 == 1397:
            print(a)
        a = v19 + CWidth
        enc = addr[count1]
        addr[count1] = 0
        bmp[a*3+0x36] = enc
        count1 +=1
        CWidth += 1

    Cheight +=1
    v19 += 3*Width


        
        
