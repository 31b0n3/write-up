.386
.model flat, stdcall
option casemap:none

.code
main proc
assume fs: nothing 
								;kernel32.dll base address
mov eax, fs:[30h]  ; PEB
mov eax, [eax+0Ch] ; Ldr
mov esi, [eax+14h] ; InMemoryOrderModuleList
lodsd			   ; eax = Value of offset esi = Flink
xchg esi,eax
lodsd			   ; eax = offset LDR_DATA_TABLE_ENTRY of kernel32.dll
add eax, 10h	   ; offset base address
mov ebx, DWORD PTR [eax] 
								; address of GetProcA

mov ecx, [ebx + 3ch]	; e_lfanew offset -> offset PE header
add ecx, ebx
mov edx, [ecx + 78h]	;offset export table
add edx, ebx			;export table 
mov esi, [edx + 20h]	
add esi, ebx			;names table


xor ecx, ecx
L1:
mov edi, 50746547h		;"GetP"

mov eax, [esi + ecx * 4] ; offset name
add eax, ebx ; name 
inc ecx
cmp DWORD PTR [eax], edi
jnz L1

mov edi,41636F72h
cmp DWORD PTR [eax + 4], edi
jnz L1


mov esi, [edx + 24h]	
add esi, ebx			; Ordinal table
mov di, WORD PTR [esi + ecx * 2]
xor ecx, ecx
mov cx, di
mov esi, [edx + 1ch]	
add esi, ebx			; Address table
dec ecx
mov edx, [esi + ecx * 4]
add edx, ebx
mov edi, edx	; edi = offset GetProcAddress

							; address of LoadLibraryA
push 0
push 41797261h	; 'aryA'
push 7262694ch	; 'Libr'
push 64616f4ch	; 'Load'

push esp
push ebx

call edi ; eax = offset LoadLibraryA
push 0
push 6c6ch		; 'll'
push 642e3233h  ; 'd.23'
push 72657355h  ; 'resU'

push esp
call eax ; eax = offset User32.dll

push 0
push 41786fh ; 'Axo'
push 42656761h ; 'Bega'
push 7373654dh   ; 'sseM'

push esp
push eax

call edi ; eax = offset MessageBoxA

push 0
push 21646ch	 ; '!dl'
push 726f576fh	 ; 'roWo'
push 6c6c6548h	 ; 'lleH'

mov edx,esp ;	lpText

push 0
push 657865h	 ; 'exe'
push 2e21646ch	 ; '.!dl'
push 726f576fh	 ; 'roWo'
push 6c6c6548h	 ; 'lleH'

mov esi,esp ; lpCaption

push 1 ; MB_OK
push esi
push edx
push 0
call eax
									; ExitProcess
push 0
push 737365h	; 'sse'
push 636f7250h	; 'corP'
push 74697845h	; 'tixE'

push esp
push ebx

call edi ; eax = offset ExitProcess

push 0
call eax

main endp
end main
