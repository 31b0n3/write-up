def  get_last_4_bit(target):
    return target&0xf


def get_first_4_bit( target):
    return (target>>4)&0xf
def Flat(input,len):
     cipher = [0]*len
     for idx in range(len - 5,len):
        first_4_bit = get_last_4_bit(input[idx])
        later_4_bit = get_first_4_bit(input[(idx+1)%len])
        
        block = (first_4_bit << 4) + later_4_bit
        cipher[idx] = input[idx]^block
     for i in range(len):
         input[i]=cipher[i]

ciphero=     [0x98,0x02,0xaa,0x9b,0xfe,0xdc,0x44,0x73,0xef,0x9d,
             0x40,0xdd,0xd8,0x05,0xc9,0xea,0x51,0xcd,0xab,0x01,
             0x77,0x14,0x8c,0x62,0x51,0xea,0x41,0xbe,0xae,0x33,
             0x23,0xd9,0x9d,0xfe,0x22,0x36,0xdb,0x23,0xfa,0x72,
             0x36,0xfd,0xb9,0xbc,0x11,0x04,0xfc,0xc8,0xdf]
flag= [0x4B,0x43,0x53,0x43,0x7B,0x7D]

while len(flag) <= 48:
    for bf in range (0x20,0xff):
        temp = [0]*(len(flag))
        for i in range (len(flag)):
            temp[i] = flag[i]
        temp.insert(len(temp)-1,bf)     
        Flat(temp,len(temp))
        Flat(temp,len(temp))
        Flat(temp,len(temp))
        Flat(temp,len(temp))
        Flat(temp,len(temp))

        if (get_last_4_bit(temp[len(temp)-5]) == get_last_4_bit(ciphero[len(temp)-5])) and (get_first_4_bit(temp[len(temp)-4]) == get_first_4_bit(ciphero[len(temp)-4])):
                flag.insert(len(flag)-1,bf) 
                break
for i in flag:
    print(chr(i),end="")