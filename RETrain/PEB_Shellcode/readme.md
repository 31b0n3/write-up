## PEB and Shellcode

PEB (Process Environment Block) là một cấu trúc dữ liệu quan trọng trong việc quản lý các tiến trình. Nó lưu trữ về thông tin của process, các thư viện được tải lên , thông tin liên quan đến việc gỡ lỗi và theo dõi process. 

Để lấy được offset của PEB thì dựa vào TIB(Thread Information Block) có offset của PEB nằm trong thanh ghi FS:[0x30] (x86) và GS:[0x60] (x64). Mình sẽ để một số link tham khảo bên dưới:

[PEB (Wikipedia)](https://en.wikipedia.org/wiki/Process_Environment_Block#:~:text=Ldr,about%20loaded%20modules)

[PEB (Geoff Chappell)](https://www.geoffchappell.com/studies/windows/km/ntoskrnl/inc/api/pebteb/peb/index.htm)

[PEB (Wordpress)](https://ntopcode.wordpress.com/2018/02/26/anatomy-of-the-process-environment-block-peb-windows-internals/#:~:text=To%20start%20off,kernel32.dll%20ourselves.)

[TIB (Wikipedia)](https://en.wikipedia.org/wiki/Win32_Thread_Information_Block)

```C++
typedef struct _PEB {
  BYTE                          Reserved1[2];
  BYTE                          BeingDebugged;
  BYTE                          Reserved2[1];
  PVOID                         Reserved3[2];
  PPEB_LDR_DATA                 Ldr;
  PRTL_USER_PROCESS_PARAMETERS  ProcessParameters;
  PVOID                         Reserved4[3];
  PVOID                         AtlThunkSListPtr;
  PVOID                         Reserved5;
  ULONG                         Reserved6;
  PVOID                         Reserved7;
  ULONG                         Reserved8;
  ULONG                         AtlThunkSListPtr32;
  PVOID                         Reserved9[45];
  BYTE                          Reserved10[96];
  PPS_POST_PROCESS_INIT_ROUTINE PostProcessInitRoutine;
  BYTE                          Reserved11[128];
  PVOID                         Reserved12[1];
  ULONG                         SessionId;
} PEB, *PPEB;
```

Bên trên là cấu trúc của PEB. Như ta có thể thấy, có rất nhiều lĩnh vực có thể khai thác, nhưng chúng ta sẽ tập trung vào một vài trường quan trọng:

- **Antidebug**
Chúng ta có thể Antidebug bằng cách kiểm tra trường `BeingDebugged`(thường là offset 0x2) chỉ định xem tiến trình đang được gỡ lỗi hay không. Bằng cách kiểm tra giá trị của trường này, chúng ta có thể thực hiện một số hành động để ngăn không cho debug. Ngoài ra chúng ta còn có thể kiểm tra trường PEB.NtGlobalFlag hoặc PEB.DebuggerPresent. Các bạn có thể xem chi tiết code mẫu tại [Anti-debugging techniques](https://users.cs.utah.edu/~aburtsev/malw-sem/slides/02-anti-debugging.pdf)

- **Resole API**
Chúng ta sử dụng PEB để giải quyết các hàm API trong quá trình thực thi một chương trình. Bằng PEB, chương trình gọi các hàm API từ các DLL để thực hiện các tác vụ cụ thể. Các link dưới đây sẽ hướng dẫn bạn từng bước một để resole API cũng như viết Shellcode:

[Finding Kernel32 Base and Function Addresses in Shellcode](https://www.ired.team/offensive-security/code-injection-process-injection/finding-kernel32-base-and-function-addresses-in-shellcode)

[Writing shellcodes for Windows x64](https://nytrosecurity.com/2019/06/30/writing-shellcodes-for-windows-x64/)

Vậy Shellcode là gì? 

Shellcode là đoạn code assembly mà trong đoạn code đó không khai báo biến hay thư viện. Chúng chạy bằng cách lấy địa chỉ hàm API để từ đó gọi hàm API để làm các tác vụ mong muốn. Vì nó không cần khai báo thư viện nên có thể hiểu rằng shellcode có thể chạy hầu hết trên bất cứ máy tính nào. Vậy nên shellcode thường dùng để tấn công mã độc máy tính. Nó được chèn vào một chương trình để thực hiện một hành động xấu nhất định . Để hiểu và viết được shellcode ta cũng cần phải biết thêm những khái niệm sau:

- [PEB_LDR_DATA](https://www.geoffchappell.com/studies/windows/km/ntoskrnl/inc/api/ntpsapi_x/peb_ldr_data.htm?tx=185)

- [Linked Lists - Flink and Blink](https://bsodtutorials.blogspot.com/2013/10/linked-lists-flink-and-blink.html)

- [Export Address Table](https://ferreirasc.github.io/PE-Export-Address-Table/)

- [WINDOWS SHELLCODE DEVELOPMENT – PART 1](https://securitycafe.ro/2015/10/30/introduction-to-windows-shellcode-development-part1/)

- [WINDOWS SHELLCODE DEVELOPMENT – PART 2](https://securitycafe.ro/2015/12/14/introduction-to-windows-shellcode-development-part-2/)



