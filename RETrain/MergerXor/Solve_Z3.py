def  get_last_4_bit(target):
    return target&0xf


def get_first_4_bit( target):
    return (target>>4)&0xf
def Flat(input,len):
     cipher = [0]*len
     for idx in range(len):
        first_4_bit = get_last_4_bit(input[idx])
        later_4_bit = get_first_4_bit(input[(idx+1)%len])
        
        block = (first_4_bit << 4) + later_4_bit
        cipher[idx] = input[idx]^block
     for i in range(len):
         input[i]=cipher[i]


from z3 import *
cipher=     [0x98,0x02,0xaa,0x9b,0xfe,0xdc,0x44,0x73,0xef,0x9d,
             0x40,0xdd,0xd8,0x05,0xc9,0xea,0x51,0xcd,0xab,0x01,
             0x77,0x14,0x8c,0x62,0x51,0xea,0x41,0xbe,0xae,0x33,
             0x23,0xd9,0x9d,0xfe,0x22,0x36,0xdb,0x23,0xfa,0x72,
             0x36,0xfd,0xb9,0xbc,0x11,0x04,0xfc,0xc8,0xdf]
formatt= [0x4B,0x43,0x53,0x43,0x7B]
flag = [BitVec(f'{i:2}',8) for i in range(len(cipher))]
S = Solver()
for i in flag:
    S.add(i > 0x20,i < 0x7f)
for f,c in zip (flag, formatt):
    S.add(f == c)
Flat(flag, len(flag))
Flat(flag, len(flag))
Flat(flag, len(flag))
Flat(flag, len(flag))
Flat(flag, len(flag))
for f,c in zip (flag, cipher):
    S.add(f == c)

S.check()
m = S.model()
model = sorted([(d, m[d]) for d in m], key = lambda x: str(x[0]))
for m in model:
     print(chr(m[1].as_long()), end='')