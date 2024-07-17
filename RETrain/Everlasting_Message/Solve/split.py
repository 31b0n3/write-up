def split(input_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    l = len(data)
    t = l // 8
    t = (t // 10) * 10
    for i in range(8):
        s = i * t
        e = (i + 1) * t
        with open(f'flag_enc_{i + 1}', 'wb') as c:
            c.write(data[s:e])

split('flag_enc')