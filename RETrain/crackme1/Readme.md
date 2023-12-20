# Crack_me1

Đề bài cho ta file [crack_me1.exe](.\chall\crack_me1.exe). Mình sẽ thử chạy file:

![](./img/Run.png)

Bài này yêu cầu ta nhập password đúng. Cho file vào DIE thì đây là file 32-bit.

![](./img/DIE.png)

Chúng ta sẽ cùng phân tích chương trình trong ida

## IDA

![](./img/Overview.png) 

Sau khi mở file bằng ida thì ta đã có thể xem luôn được mã giả C. 

![](./img/p1.png)

Ở phần đầu, chương trình sẽ đặt tất cả các phần tử mảng của `v6`, `v7` = 0.

`v8` được gán địa chỉ của `unk_404BE8`nhưng `v8` chỉ xuất hiện mỗi chỗ đó nên ta tạm thời bỏ qua. Tiếp đến in ra giá trị của biến `Format`.

`sub_4014D0("%300[^\n]s", (char)&v5);` dòng này yêu cầu chúng ta nhập kí tự vào địa chỉ của `v5`; `%300[^\n]` nghĩa là chúng ta được phép nhập tối đa 300 kí tự và kết thúc đọc khi gặp `\n`.

![](./img/p2.png)

`v7` là địa chỉ lưu trữ kí tự thứ 1 ;`v6` là địa chỉ lưu trữ kí tự thứ 2 ta nhập vào. Do đó, cả đoạn code này chỉ là tính chiều dài `password` ta nhập vào.

![](./img/p3.png)

Sau đó, chương trình check xem độ dài `password` có >= 294 không. Nếu không thì print ra và kết thúc chương trình. Còn ngược lại thì sẽ gọi hàm `sub_1211D0` với tham số truyền vào là địa chỉ của `v5`(Địa chỉ lưu trữ `password` ta nhập vào)

![](./img/p4.png)

Đây là hàm `sub_1211D0`. Đầu tiên, `v3` được gán địa chỉ của`unk_404BE8`; sau đó kiểm tra password ta nhập vào có nhỏ hơn 55 không. Nếu không thì thực hiện vòng lặp for bên dưới.

![](./img/p5.png)

Bắt đầu vòng lặp, chương trình gọi hàm `sub_121080` và truyền vào 3 tham số: (giá trị tại địa chỉ `v3`, địa chỉ của password ta nhập vào, địa chỉ của `v3` + 2)

![](./img/p6.png)

Ta thấy `v5`, `v6`,`lpAddress` được gán với giá trị trả về của hàm `sub_121000` nên ta sẽ vào phân tích hàm này:

![](./img/p7.png)





