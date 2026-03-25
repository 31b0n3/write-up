# FSOP

## Giới thiệu

- FILE là một struct để miêu tả đặc tính của các file được mở trong chương trình. Nó được khởi tạo như khi chạy hàm `fopen()` và nó giá trị của nó ở trên heap.

- FILE struct được định nghĩa như sau:

```c
struct _IO_FILE
{
  int _flags;		/* High-order word is _IO_MAGIC; rest is flags. */

  /* The following pointers correspond to the C++ streambuf protocol. */
  char *_IO_read_ptr;	/* Current read pointer */
  char *_IO_read_end;	/* End of get area. */
  char *_IO_read_base;	/* Start of putback+get area. */
  char *_IO_write_base;	/* Start of put area. */
  char *_IO_write_ptr;	/* Current put pointer. */
  char *_IO_write_end;	/* End of put area. */
  char *_IO_buf_base;	/* Start of reserve area. */
  char *_IO_buf_end;	/* End of reserve area. */

  /* The following fields are used to support backing up and undo. */
  char *_IO_save_base; /* Pointer to start of non-current get area. */
  char *_IO_backup_base;  /* Pointer to first valid character of backup area */
  char *_IO_save_end; /* Pointer to end of non-current get area. */

  struct _IO_marker *_markers;

  struct _IO_FILE *_chain;

  int _fileno;
  int _flags2;
  __off_t _old_offset; /* This used to be _offset but it's too small.  */

  /* 1+column number of pbase(); 0 is unknown. */
  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];

  _IO_lock_t *_lock;
  __off64_t _offset;
  /* Wide character stream stuff.  */
  struct _IO_codecvt *_codecvt;
  struct _IO_wide_data *_wide_data;
  struct _IO_FILE *_freeres_list;
  void *_freeres_buf;
  size_t __pad5;
  int _mode;
  /* Make sure we don't get into trouble again.  */
  char _unused2[15 * sizeof (int) - 4 * sizeof (void *) - sizeof (size_t)];
};

```

FILE structure sẽ được kết nối với những structure khác thông qua linked_list đại diện bằng ` _IO_list_all`:

![](./img/IO_list_all.png)

- Khi mà ta chạy chương trình thì File struct của stdin, stdout, stderr sẽ ở trên libc thay vì ở vùng nhớ heap như khi ta mở file bằng `fopen()`

`vtable` là bảng chứa con  trỏ đến các hàm sẽ được các hàm khác như `fwrite`,`fread`,... gọi qua `vtable` mà không gọi trực tiếp

- `FSOP` là viết tắt của `File Stream Oriented Programming` (lập trình hướng luồng tệp)

- Vì nó có thể hướng luồng tệp nên nếu ta có thể thay đổi được các giá trị của file struct, ta có thể khai thác.

## Một số cách khai thác cơ bản

1. `Kỹ thuật Arbitrary Read`

- Đây là một kỹ thuật lợi dụng hàm `fread()` để bắt chương trình đọc dữ liệu vào địa chỉ target

- Bình thường, hàm `fread()` sẽ đọc dữ liệu từ tệp vào vùng nhớ giữa `buff_base` và `buff_end`. Nếu không đủ dữ liệu thì nó sẽ cấp phát bộ đệm mới và gán vào các trường đó địa chỉ mới và đọc tiếp.

- Vậy nếu ta có thể overwrite được file struct, hoàn toàn ta có thể thay đổi địa chỉ tại `buff_base` và `buff_end` thành địa chỉ mà ta muốn.

- Để cho kỹ thuật này thành công thì ta cần thỏa mãn 1 số điều kiện:

    - `Flags` set value cho phép đọc

    - `read_ptr` = `read_end` 
    
    - `buff_end - buff_base` > số byte ta muốn đọc vào.

Ví dụ : [FSOP1](./chall/fsop1/)

2. `Kỹ thuật Arbitrary Write`

- Tương tự như trên, ta có thể điểu chỉnh các địa chỉ để chương trình thay vì ghi dữ liệu vào file thì ta có thể ghi ra ngoài màn hình hoặc tệp của chúng ta

- Điều kiện để thành công:

    - Flag cho phép ghi

    - kích thước `buff_end - buff_base` đủ lớn

    - `read_end` = `write_base` trỏ đến dữ liệu mà ta muốn in ra

    -`write_ptr` trỏ đến địa chỉ kết thúc.

3. `Thay đổi vtable để chương trình thực thi hàm mà ta muốn`

- Như ta đã biết thì khi thực hiện các hàm như `fread()`, `fwrite()` thì chương trình sẽ gọi các hàm `IO` thông qua `vtable` nên nếu ta thay đổi được địa chỉ của trường vtable trỏ đến `fake_vtable` của ta thì ta sẽ đánh lừa được chương trình thực thi hàm mà ta muốn

- Tuy nhiên ở các phiên bản libc mới, libc kiểm tra các điều kiện nghiêm ngặt hơn,kiểm tra xem địa chỉ `vtable` xem có ở trên vùng `vtable` của libc hay không,`vtable` nằm dưới `_lock` nên ta phải set lại trường `_lock` sao cho thỏa mãn phải là một địa chỉ writeable và có giá trị = 0.:


- Tuy nhiên vẫn có lỗ hổng để ta có thể trỏ đến `_fake_vtable` của ta đó là thay đổi địa chỉ `_wide_data` đến `fake_wide_data` của chúng ta.

- Khi mà chương trình thực thi hàm `_IO_wfile_overflow`, hàm đó sẽ gọi tiếp đến `_IO_wdoallocbuf`, hàm này sẽ sử dụng `wide_data`.Bản chất `wide_data` là một con trỏ tới một cấu trúc khác:

```c
struct _IO_wide_data
{
  wchar_t *_IO_read_ptr;	/* Current read pointer */
  wchar_t *_IO_read_end;	/* End of get area. */
  wchar_t *_IO_read_base;	/* Start of putback+get area. */
  wchar_t *_IO_write_base;	/* Start of put area. */
  wchar_t *_IO_write_ptr;	/* Current put pointer. */
  wchar_t *_IO_write_end;	/* End of put area. */
  wchar_t *_IO_buf_base;	/* Start of reserve area. */
  wchar_t *_IO_buf_end;		/* End of reserve area. */
  /* The following fields are used to support backing up and undo. */
  wchar_t *_IO_save_base;	/* Pointer to start of non-current get area. */
  wchar_t *_IO_backup_base;	/* Pointer to first valid character of
				   backup area */
  wchar_t *_IO_save_end;	/* Pointer to end of non-current get area. */

  __mbstate_t _IO_state;
  __mbstate_t _IO_last_state;
  struct _IO_codecvt _codecvt;

  wchar_t _shortbuf[1];

  const struct _IO_jump_t *_wide_vtable;
};


```
 Như ta thấy thì struct này cũng chứa một con trỏ `vtable` của riêng nó. Vậy nên nếu ta thay đổi thành `fake_wide_data` của ta rồi từ đó kiểm soát `vtable` => hàm `_IO_wdoallocbuf` sẽ lấy `vtable` từ struct đó gọi hàm mà không kiểm tra bảo mật

 - Vậy để thực hiện được hàm `_IO_wfile_overflow` thì ta sẽ thay đổi vtable thành địa chỉ của `_IO_wfile_jumps` để khi chương trình nảy tới `r15 + 0x38` thì sẽ nhảy vào hàm `_IO_wfile_xsputn`:

 ![](./img/vtable.png)

- Từ đó gọi được `_IO_wfile_overflow` -> `_IO_wdoallocbuf` -> lấy con trỏ `_fake_wide_data` và lấy `fake_vtable` trong đó. Từ đó sẽ gọi hàm trong `vtable` đó.


