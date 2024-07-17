### MAP INPUTS TO OUTPUTS ###
# import GDB stuff
import gdb
ge = gdb.execute
parse = gdb.parse_and_eval
import json

# set up break points
BASE = 0x00555555554000
FUNCS = []
FUNCS.append(BASE+0x12e9)
FUNCS.append(BASE+0x264d)
FUNCS.append(BASE+0x3977)
FUNCS.append(BASE+0x4c0e)

# set up debugging
ge('aslr off')
ge('file messages')
ge('b open')
ge('run input output8')
ge('finish')


# get output for each possible 5-nibble input
for x, func in enumerate(FUNCS):
    output = []
    for i in range(0xfffff):
        if i % 0x1000 == 0:
            print(hex(i))
        inp = i
        out = ge(f'call ((long(*)(long)){func})({hex(inp)})', to_string=True).split(' = ')[1].strip()
        output.append(out)
    
    with open(f'output{x}.json', 'w') as f:
        json.dump(output, f)