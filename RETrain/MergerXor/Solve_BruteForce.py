def  get_last_4_bit(target):
    return target&0xf


def get_first_4_bit( target):
    return (target>>4)&0xf
cipher = [[0 for _ in range(49)] for _ in range(6)]
cipher[0] = [0x98,0x02,0xaa,0x9b,0xfe,0xdc,0x44,0x73,0xef,0x9d,
             0x40,0xdd,0xd8,0x05,0xc9,0xea,0x51,0xcd,0xab,0x01,
             0x77,0x14,0x8c,0x62,0x51,0xea,0x41,0xbe,0xae,0x33,
             0x23,0xd9,0x9d,0xfe,0x22,0x36,0xdb,0x23,0xfa,0x72,
             0x36,0xfd,0xb9,0xbc,0x11,0x04,0xfc,0xc8,0xdf]
flag=[0x4B,0x43,0x53,0x43,0x7B]
lengh= len(cipher[0])
last = [0]* lengh
now = [0]*lengh
pbf=[0]*5
o=0
while o < 5:
    check = 0
    if pbf[o]<0x10:
        for bf in range(pbf[o],0x10):

            for i in range(lengh):
                last[i]=cipher[o][i]
            now[lengh-1]=bf
            for u in range(lengh-1,-1,-1):
                temp=get_first_4_bit(last[u])^now[u]
                now[u] += (temp*0x10)
                if u != 0:
                    now[u-1] = get_first_4_bit(now[u])^get_last_4_bit(last[u-1])
                else:
                    if get_last_4_bit(now[u-1]) == get_first_4_bit(now[u])^get_last_4_bit(last[u-1]):
                        check = 1
                        pbf[o]=bf+1

                        for p in range(lengh):
                            cipher[o+1][p]= now[p]



            if check:
                if o ==4:
                    count =0
                    for q in range(5):
                        if cipher[o+1][q] == flag[q]:
                            count +=1
                    if count == 5:
                        for i in range(lengh):
                            print(chr(cipher[o+1][i]),end="")
                        o+=1
                else:    
                    o+=1
                    break
            else:
                o-=1
                break
    else:
        pbf[o]=0
        o-=1      

        
