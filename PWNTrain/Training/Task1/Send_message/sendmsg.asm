BITS 64
GLOBAL _start

SECTION .data
sockaddr:
    dw 2    ;AF_INET
    dw 0x3930;  port 12345
    dd 0x0100007f ; 127.0.0.1 
    dq 0

guide db "PLEASE ENTER MESSAGE TO SEND TO SEVER: " , 0
success db "I received your message. The message is: " , 0
SECTION .bss

input resb 100
inputlen resq 1
recvmsg resb 100
socklen resb 1

SECTION .text
_start:

    ;WRITE GUIDE
    mov rax,0x01        ;write() opcode
    mov rdi,1           ; 1: stdout
    lea rsi,[guide]     ; buf offset
    mov rdx, 39         ; len buf
    syscall

    ;READ USER INPUT
    xor rax,rax         ;read() opcode
    mov rdi,0           ; 0: stdin
    lea rsi,[input]     ; buf offset
    mov rdx, 100        ; strlen
    syscall
    mov byte[inputlen],al 

sever:
    ;socket() : create socket have ability connect with localhost
    mov rax,0x29
    mov rdi,2       ;AF_INET 
    mov rsi,1       ;SOCK_STREAM
    mov rdx,0       ;protocol can set to 0
    syscall
    mov r14,rax     ; store sockfd in r14 register for later use
    

    ;BIND() to connect socket with address was set in sockaddr
    mov rdi,r14         ;sockfd of socket we want to connect
    mov rax, 0x31
    lea rsi,[sockaddr]
    mov rdx,16          ; size of sockaddr
    syscall

    ;LISTEN() to mark this socket as passive socket to listen incoming connection request
    mov rax,0x32
    mov rsi,3       ; max 3 request in queue
    syscall

    create_fork:  

        ;parent fork is used for accept request, receive message and print that message
        ;child fork is used for connect to sever and send message 

        mov rax,0x39
        syscall
        mov rbx,rax

        cmp rbx,0           ; check fork
        je client

    ;ACCEPT() : to accept request connection from client
    mov rax,0x2b
    lea rsi,[sockaddr]      
    mov BYTE[socklen],16
    lea rdx,[socklen]       ; This field need address of sockaddr lenght, not lenght of sockaddr
    syscall

    ;READ(recv from socket) : read message from client 
    mov rdi,rax   ; new socketfd returned by accept()
    xor rax,rax
    lea rsi,[recvmsg]
    mov rdx,100
    syscall
    
    ;cmp rax,0          ; if read fail -> exit
    ;jl exit

    ;WRITE SUCCESS      ; else write success msg and user msg
    mov rax,0x01
    mov rdi,1
    lea rsi,[success]
    mov rdx, 41
    syscall

    ;WRITE MSG
    mov rax,0x01
    mov rdi,1
    lea rsi,[recvmsg]
    mov rdx, [inputlen]
    syscall

    cmp rbx,0           ; exit parent fork
    jne exit

client:

    ;socket() :  create another socket for connect to sever
    mov rax,0x29
    mov rdi,2       ;AF_INET
    mov rsi,1
    mov rdx,0
    syscall
    mov r14,rax

    ;Connect() :  Send connection request to sever
    mov rdi,r14
    lea rsi,[sockaddr]
    mov rdx,16
    mov rax,0x2a
    syscall


    ;WRITE : Send message to sever
    mov rax,0x01
    mov rdi,r14
    lea rsi,[input]
    mov rdx,[inputlen]
    syscall

exit:
    xor rdi,rdi
    mov rax,0x3c
    syscall

; sever: create socket -> bind to addr in sockaddr -> listen connection request -> accept connection -> recv msg
; client: create socket -> connect to addr in sockaddr -> send msg



