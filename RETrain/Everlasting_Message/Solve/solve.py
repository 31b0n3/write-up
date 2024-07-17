import sys

arg = int(sys.argv[1])


### SETUP ###
# imports
import json

# load the outputs
func1_out = json.load(open('output0.json'))
func2_out = json.load(open('output1.json'))
func3_out = json.load(open('output2.json'))
func4_out = json.load(open('output3.json'))

# convert the outputs to a dictionary
func1_out = {int(v,16): x for x, v in enumerate(func1_out)}
func2_out = {int(v,16): x for x, v in enumerate(func2_out)}
func3_out = {int(v,16): x for x, v in enumerate(func3_out)}
func4_out = {int(v,16): x for x, v in enumerate(func4_out)}



### HELPER FUNCTIONS ###
import itertools

def flip_bits(n, bit_positions):
    """Flip the bits in `n` at the positions specified in `bit_positions`."""
    for pos in bit_positions:
        n ^= (1 << pos)
    return n

def generate_possibilities(initial_value):
    bit_length = 40  # 5 bytes = 40 bits
    bit_positions = range(bit_length)
    flipped_values = []

    # Generate all combinations of 2 bit positions||tao to hop 2 bit
    for pos1, pos2 in itertools.combinations(bit_positions, 2):
        # Create a copy of the initial value
        new_value = flip_bits(initial_value, [pos1, pos2])
        flipped_values.append(new_value)

    # generate all combinations of 1 bit positions
    for pos in bit_positions:
        new_value = flip_bits(initial_value, [pos])
        flipped_values.append(new_value)

    return flipped_values+[initial_value]



### SOLVE ###
# split flag_enc into 20-byte chunks
enc = open(f'flag_enc_{arg}', 'rb').read()
chunks = [enc[i:i+20] for i in range(0, len(enc), 20)]

print("Starting")

for chunk in chunks:
    #print(chunk)
    # steps 1 & 2
    func1 = int.from_bytes(bytes.fromhex(chunk[0:5].hex()),'little')
    func2 = int.from_bytes(bytes.fromhex(chunk[5:10].hex()),'little')
    func3 = int.from_bytes(bytes.fromhex(chunk[10:15].hex()),'little')
    func4 = int.from_bytes(bytes.fromhex(chunk[15:20].hex()),'little')

    # calculate possibilities for func1 (2 random bit flips)
    for x in generate_possibilities(func1):
        if func1_out.get(x, None) is not None:
            y = func1_out.get(x, None)
            break
    else:
        print('Failed to find func1',chunk)
        y = 0xfffff

    # calculate possibilities for func2 (2 random bit flips)
    for x in generate_possibilities(func2):
        if func2_out.get(x, None) is not None:
            x = func2_out.get(x, None)
            break
    else:
        print('Failed to find func2',chunk)
        x = 0xfffff
    #ghép byte và chuyển về dạng little edian
    b = bytes.fromhex(hex(int.from_bytes(bytes.fromhex(hex(x << 20 | y)[2:].zfill(10)),'little'))[2:].zfill(10))
    with open(f'flag_{arg}','ab') as f:
        f.write(b)

    

    # calculate possibilities for func3 (2 random bit flips)
    for x in generate_possibilities(func3):
        if func3_out.get(x, None) is not None:
            y = func3_out.get(x, None)
            break
    else:
        print('Failed to find func3',chunk)
        y = 0xfffff

    # calculate possibilities for func4 (2 random bit flips)
    for x in generate_possibilities(func4):
        if func4_out.get(x, None) is not None:
            x = func4_out.get(x, None)
            break
    else:
        print('Failed to find func4',chunk)
        x = 0xfffff

    b = bytes.fromhex(hex(int.from_bytes(bytes.fromhex(hex(x << 20 | y)[2:].zfill(10)),'little'))[2:].zfill(10))
    with open(f'flag_{arg}','ab') as f:
        f.write(b)