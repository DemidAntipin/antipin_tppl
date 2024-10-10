%macro pushd 0
   push rax
   push rbx
   push rcx
   push rdx
%endmacro

%macro popd 0
   pop rdx
   pop rcx
   pop rbx
   pop rax
%endmacro

%macro print 2
   pushd
   mov rax, 1
   mov rdi, 1
   mov rsi, %1
   mov rdx, %2
   syscall
   popd
%endmacro

%macro dprint 0
   pushd
   mov rbx, 0
   mov rcx, 10
   %%divide:
       xor rdx, rdx
       div rcx
       push rdx
       inc rbx
       cmp rax, 0
       jne %%divide

   %%digit:
       pop rax
       add rax, '0'
       mov [result], al
       print result, 1
       dec rbx
       cmp rbx, 0
       jg %%digit
   popd
%endmacro

section .text
global _start

_start:
initial_x1:
   mov eax, dword [num]
   mov dword [x1_num], eax
   mov dword [x1_den], dword 2
x2:
   xor rax, rax
   mov eax, dword [num]
   mul dword [x1_den]
   mul dword [x1_den]
   mov dword [x2_num], eax
   mov eax, dword [x1_num]
   mul dword [x1_num]
   add dword [x2_num], eax
   mov eax, dword [x1_num]
   mul dword [x1_den]
   mov rcx, 2
   mul rcx
   mov dword [x2_den], eax
   mov eax, dword [x2_num]
   div dword [x2_den]
   mov dword [x2_num], eax
   mov dword [x2_den], dword 1
check:
   mov eax, dword [x2_num]
   mul dword [x1_den]
   mov edx, eax
   mov eax, dword [x1_num]
   sub eax, edx
   cmp eax, dword [x1_den]
   jl end
x1:
   mov edx, dword [x2_num]
   mov [x1_num], edx
   mov edx, dword [x2_den]
   mov [x1_den], edx
   jmp x2
end:
   mov eax, dword [x2_num]
   dprint
   print newline, nlen
   print done, len
   print newline, nlen
   mov rax, 60
   xor rdi, rdi
   syscall

section .data
   num dd 256

   done db 'Done', 0xA, 0xD
   len equ $ - done
   newline db 0xA, 0xD
   nlen equ $ - newline

section .bss
   result resb 1
   x1_num resd 1
   x1_den resd 1
   x2_num resd 1
   x2_den resd 1

