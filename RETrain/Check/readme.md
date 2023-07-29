# Check_1

## Overview

Bài cho file python check.py và Format Flag: ictf{}

```python
#!/usr/bin/env python3

def enc(b):
 a = [n for n in range(b[0]*2**24+b[1]*2**16+b[2]*2**8+b[3]+1)][1:]
 c,i = 0,0
 while len([n for n in a if n != 0]) > 1:
  i%=len(a)
  if (a[i]!=0 and c==1):
   a[i],c=0,0
  if (a[i] != 0):
   c+=1
  i += 1
 return sum(a)

print(r"""
    .----.   @   @
   / .-"-.`.  \v/
   | | '\ \ \_/ )
 ,-\ `-.' /.'  /
'---`----'----'
""")
flag = input("Enter flag here: ").encode()
out = b''
for n in [flag[i:i+4] for i in range(0,len(flag),4)]:
  out += bytes.fromhex(hex(enc(n[::-1]))[2:].zfill(8))

if out == b'L\xe8\xc6\xd2f\xde\xd4\xf6j\xd0\xe0\xcad\xe0\xbe\xe6J\xd8\xc4\xde`\xe6\xbe\xda>\xc8\xca\xca^\xde\xde\xc4^\xde\xde\xdez\xe8\xe6\xde':
 print("[*] Flag correct!")
else:
 print("[*] Flag incorrect.")
```

Đây là josephus problem nhưng khi làm bài thì mình chưa biết. 
Nhìn tổng thể thì bài yêu cầu chúng ta nhập flag và mã hoá, xử lý flag đó và đến cuối cùng so sánh với chuỗi có sẵn. Nếu đúng thì cho biết rằng flag đó đúng.

## Detail

```python
print(r"""
    .----.   @   @
   / .-"-.`.  \v/
   | | '\ \ \_/ )
 ,-\ `-.' /.'  /
'---`----'----'
""")
flag = input("Enter flag here: ").encode()
```

Đầu tiên, chương trình sẽ in ra con ốc sên cute và bảo chúng ta nhập flag và dùng hàm encode() để chuyển flag về dạng byte và lưu vào `flag`

`for n in [flag[i:i+4] for i in range(0,len(flag),4)]:` 

flag[i:i+4]: để lấy 4 phần tử từ flag[i]
Vậy chương trình dùng vòng lặp for để lấy 4 phần tử của mảng flag để xử lý
`out += bytes.fromhex(hex(enc(n[::-1]))[2:].zfill(8))`

`n[::-1]`: đảo ngược chuỗi
`[2:]`: Loại bỏ 2 phần tử đầu. Ở đây là để xoá tiền tố "0x,0b,..."
`zfill(8)`: Thêm số 0 vào bên trái để đủ 8 chữ số

Tóm lại, chương trình gọi hàm enc(với đầu vào là 4 kí tự đã đảo ngược), sau đó loại bỏ tiền tố của kết quả trả về và sử dụng hàm zfill để làm đầy bên trái bằng số 0 cho đủ 8 chữ số. Rồi lấy kết quả chuyển đổi về hex xong từ hex chuyển về dạng byte và lưu giá trị vào out

**Hàm enc()**

```python
def enc(b):
 a = [n for n in range(b[0]*2**24+b[1]*2**16+b[2]*2**8+b[3]+1)][1:]
 c,i = 0,0
 while len([n for n in a if n != 0]) > 1:
  i%=len(a)
  if (a[i]!=0 and c==1):
   a[i],c=0,0
  if (a[i] != 0):
   c+=1
  i += 1
 return sum(a)
```
`b[0]*2**24+b[1]*2**16+b[2]*2**8+b[3]+1`: Mục đích là để ghép 4 với nhau. Vậy dòng đầu tiên là tạo ra mảng a có số phần tử là kết quả sau khi ghép 4 byte và [1:] là cắt phần tử đầu = 0
`while len([n for n in a if n != 0]) > 1:`: kích thước của mảng a (không tính các phần tử = 0) > 1 thì điều kiện đúng, nói cách khác là vòng lặp kết thúc khi a còn 1 phần tử khác 0
`i%len(a)`: i không vượt quá độ dài của a
Vậy vòng lặp while này sẽ gán các phần tử của mảng a bằng 0 đến khi a còn 1 phần tử khác 0 cuối cùng => hàm enc() trả về phần tử cuối cùng của mảng a

```python
if out == b'L\xe8\xc6\xd2f\xde\xd4\xf6j\xd0\xe0\xcad\xe0\xbe\xe6J\xd8\xc4\xde`\xe6\xbe\xda>\xc8\xca\xca^\xde\xde\xc4^\xde\xde\xdez\xe8\xe6\xde': 
```
=> Vậy các giá trị trả về sẽ so sánh với chuỗi byte đã cho trước. Do mỗi giá trị trả về là 4 phần tử nên ta sẽ phân tách chuỗi byte cho trước thành:
```python
b'L\xe8\xc6\xd2  f\xde\xd4\xf6  j\xd0\xe0\xca  d\xe0\xbe\xe6  J\xd8\xc4\xde  `\xe6\xbe\xda  >\xc8\xca\xca  ^\xde\xde\xc4  ^\xde\xde\xde  z\xe8\xe6\xde'
```
Chuyển sang dạng int:
`1290323666 1725879542 1792073930 1692450534 1255720158 1625734874 1053346506 1591664324 1591664350 2062083806 `

Vì format flag là ictf{} nên 4 kí tự đầu là ictf. Từ đó ta có thể suy ra rằng b = b'ftci'
=> `b[0]*2**24+b[1]*2**16+b[2]*2**8+b[3]+1` = 1718903657
Do số quá lớn nên mình có viết script python để tìm ra được quy luật của hàm enc():

```python
for o in range(1,150):
    
    a = [0] * o
    for i in range(len(a)) :
        a[i]=i+1
    c,i = 0,0
    while len([n for n in a if n != 0]) > 1:
        i%=len(a)
        if (a[i]!=0 and c==1):
            a[i],c=0,0 
        if (a[i] != 0):
            c+=1
        i += 1
    print( o,": ", sum(a))
    o += 1
```
Chương trình in ra kết quả như sau:

![](/img/While.png)

Nhìn vào output thì mình suy ra quy luật của hàm enc() là khi số nhập vào tăng thêm 1 thì output sẽ tăng thêm 2, output = 1 khi input = output. Ta thấy output = 1 khi input là luỹ thừa của 2. Từ đó mình viết được hàm để reverse 
```python
def Josephus_solver(lena):
    x=1

    while lena/2 > 2**x -2**(x-1):      
        x+=1
    if lena%2 == 0:
        return int(lena/2 + 2**(x-1))
    else:
        return int((lena-1)/2 + 2**(x-1))

def decimal_to_binary(decimal_number):
    # Chuyển từ số thập phân sang nhị phân và xóa tiền tố '0b'
    binary_string = bin(decimal_number)[2:]
    return binary_string.zfill(32)  # Đảm bảo chuỗi có 32 bit

def split_into_8_bit(binary_string):
    # Tách chuỗi nhị phân thành các nhóm 8 bit
    return [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

def binary_to_ascii(binary_string):
    # Chuyển chuỗi nhị phân thành ký tự ASCII
    decimal_value = int(binary_string, 2)
    return chr(decimal_value)

# Ví dụ:
def intochar(b):
    decimal_number = b
    binary_result = decimal_to_binary(decimal_number)
    # Tách thành các nhóm 8 bit
    binary_parts = split_into_8_bit(binary_result)
    # Chuyển từng nhóm 8 bit thành ASCII
    for i in range(len(binary_parts)-1,-1,-1) :
        part = binary_parts[i]
        print(binary_to_ascii(part),end ="")
    


a = [1290323666,1725879542,1792073930,1692450534,1255720158,1625734874,1053346506,1591664324,1591664350,2062083806 ]
for i in a:
    intochar(Josephus_solver(i)) 
```
Sau khi run thì chương trình trả về flag:
`ictf{josephus_problem_speed?booooooost}`
Tìm hiểu thì biết dấu `?` trong flag sai nên chắc nó ở nấc sau nên mình thử thay đổi sang nấc 2 bằng cách thêm điều kiện ở vòng while:
```python
while lena/2 > 2**x -2**(x-1):      
        x+=1
    if lena%2 == 0:
        if lena == 1053346506 :
            return int(lena/2 + 2**(x))
        else:
            return int(lena/2 + 2**(x-1))
    else:
        return int((lena-1)/2 + 2**(x-1))
```
 Thì ra được flag như này:
`ictf{josephus_problem_speed_booooooost}`










