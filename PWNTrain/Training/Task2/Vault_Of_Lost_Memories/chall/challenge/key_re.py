cipher = "cLVQjFMjcFDGQ"
afterxor =""
for ch in cipher:
    afterxor += chr(ord(ch)^0x35)

result = ""
for c in afterxor:
    if (c <= 'z' and c >='a'):
        tmp = ord(c) - ord('a')
        if tmp <= 9:
            result += chr(tmp + 26 -10 + ord('a'))
        else:
            result += chr(tmp -10 + ord('a'))
              
    elif (c <= 'Z' and c >= 'A'):
        tmp = ord(c) - ord('A')
        if tmp <= 9:
            result += chr(tmp + 26 -10 + ord('A'))
        else:
            result += chr(tmp -10 + ord('A'))
    else:
        result += c


print(result)