cipher="l5{0v0Y7fVf?u>|:O!|Lx!o$j,;f"
print("HTB{",end="")
for i in range(len(cipher)):
    print(chr(ord(cipher[i])^i),end="")