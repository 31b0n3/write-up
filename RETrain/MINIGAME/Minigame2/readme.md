![alt text](image.png)

Ban đầu dựa trên keyword mình tìm ra được kênh youtube

![alt text](image-1.png)

Mình thấy có một video bị ẩn

![alt text](image-2.png)

copy link playlist thì mình tìm được ra id của video ẩn đó

![alt text](image-3.png)

mình tìm thử web archive xem có gì không và ta đã có part 1:

![alt text](image-4.png)

ta đã có 

**Part1: KCSC{cHuC_C4c_b4n**

tìm ra được đoạn mã, giải encode ra thì ta có link

![alt text](image-5.png)

https://cybersharing.net/s/d22fdbeca940c94d


![alt text](image-6.png)

Mở file mp4 thì ta thấy hình ảnh trường KMA (miền bắc)

Tìm thử đánh giá trên google map:

![alt text](image-7.png)

ta ra được :

**Part 2: _614n6_51nh_Vu1**

![alt text](image-8.png)

tìm kiếm trên các trang thì mình tìm được link github

![alt text](image-9.png)
ở đây có 1 file

![alt text](image-10.png)

tuy nhiên khi mình xem commit thì mình nhìn được key là part 3, đồng thời có file encrypt, tải về và nhờ AI gen code ra để tạo file zip :

```python
def solve_puzzle():
    # The hex output provided
    hex_data = "002a717034333a205776b3c7f868b66baf2fdc5f6d342957623463506172044c52534e2b134b2b42470d2ba71b7c764582ab884d1b4187cabe5b0d1a776a8a3dfd90b91c3a7325fde570de414c56ad3de3789338db14d2df3adad5434be2f124676674b48feb15fee8061e4a4fbfde24b2424253f934523606ad37aeafee3e4a3f2a9701f8a3c000130a21beb1777e3d1899c22f491b3d0a3dfd06cda4e5ce6da037c0c8e2e9b1cc4af7bd4a3680643c303b6c3305146c36665f76346e506972f4b8a761e36bb52fd66c33750f643355526d10795f62346e5061527420333a205f7643330d5a1b2b094b2171194c0d5562146e5061727421332220b7341ae5c442a95e611cbbf5c445a55e60e2a61dc603a8216371255976335f6c32755e6c6c555f6d80795f62346e"
    
    # The key found in the original source code
    key = "Part 3: _v3_l3u_l3U_m4y_b4n"
    key_bytes = key.encode("utf-8")
    
    # Convert hex to bytes
    encrypted_bytes = bytes.fromhex(hex_data)
    
    decrypted_bytes = bytearray(len(encrypted_bytes))
    key_len = len(key_bytes)
    
    # Perform XOR to decrypt
    for i, b in enumerate(encrypted_bytes):
        decrypted_bytes[i] = b ^ key_bytes[i % key_len]
        
    # Check for ZIP signature (PK..)
    if decrypted_bytes.startswith(b'\x50\x4B\x03\x04'):
        print("[+] Detected ZIP file header.")
        output_filename = "secret_result.zip"
    else:
        print("[!] Warning: Unknown file type.")
        output_filename = "secret_result.bin"
        
    # Write to file
    with open(output_filename, "wb") as f:
        f.write(decrypted_bytes)
        
    print(f"[+] Decrypted file saved as: {output_filename}")
    print("[+] Please unzip this file to see the contents.")

if __name__ == "__main__":
    solve_puzzle()
```
![alt text](image-11.png)


**Part 3: _v3_l3u_l3U_m4y_b4n**

ở đây ta ra 1 link rickroll

tuy nhiên chưa hết file

![alt text](image-12.png)

ở đuôi file ta được thế này

nghĩ đến vậy ta thử thêm đuôi patch vào link commit github:

![alt text](image-13.png)

ta có username

kiếm trên tiktok ta ra được part 4:

![alt text](image-14.png)

**Part 4: _kh0n6_c0_ny**

![alt text](image-15.png)

Có hint gần tòa vtc

![alt text](image-16.png)

Ta tìm ra được KMA miền nam gần đó

![alt text](image-17.png)

Tìm review thì thấy được thế này

![alt text](image-18.png)

dùng AI ta giải ra được ý nghĩa

từ đó nhờ AI viết ta được:

![alt text](image-19.png)

![alt text](image-20.png)

Trong link có 2 file ảnh

Ta sử dụng AI để xor 2 ảnh vào:

```python
from PIL import Image, ImageChops

# Mở hai hình ảnh
img1 = Image.open('B.png')
img2 = Image.open('FB.png')

# Đảm bảo cả hai ảnh cùng kích thước và chế độ màu
if img1.size == img2.size:
    # Thực hiện phép XOR (hoặc dùng hàm difference để tìm sự khác biệt)
    # Trong xử lý ảnh, Difference thường tương đương XOR về mặt hiển thị
    result = ImageChops.logical_xor(img1.convert('1'), img2.convert('1')) 
    # Nếu ảnh màu, dùng difference:
    result_color = ImageChops.difference(img1, img2)
    
    # Lưu và hiển thị kết quả
    result_color.save('flag_solved.png')
    result_color.show()
    print("Đã xử lý xong! Hãy kiểm tra file flag_solved.png")
else:
    print("Hai hình ảnh không cùng kích thước!")
```

![alt text](flag_solved.png)

yay ta đã có được part 5:

**Part 5: d1_ch01_n031_:3}**

FLAG: `KCSC{cHuC_C4c_b4n_614n6_51nh_Vu1_v3_l3u_l3U_m4y_b4n_kh0n6_c0_ny_d1_ch01_n031_:3}`

