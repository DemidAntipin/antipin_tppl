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
       mov [result], rax
       print result, 1
       dec rbx
       cmp rbx, 0
       jg %%digit
   popd
%endmacro

section .text
global _start


_start:
   ; Открываем файл в режиме чтения
   mov rax, 2
   mov rdi, filename
   mov rsi, 0
   syscall

   ; Проверяем, если файл не может быть открыт
   cmp rax, 0
   jl error

   ; Читаем данные из файла
   mov rdi, rax
   mov rsi, buffer
   mov rdx, 1024
   mov rax, 0
   syscall

   ; Проверяем, если чтение данных не удалось
   cmp rax, 0
   jl error

   ; Закрываем файл
   mov rax, 3
   mov rdi, rax
   syscall

   ; Парсим первую строку и записываем в массив x
   xor rax, rax
   xor rbx, rbx
   xor rcx, rcx
   xor rdx, rdx
fill_x:
   cmp rcx, xlen
   je end_x
   mov dl, [buffer+rbx]
   inc rbx
   sub edx, '0'
   cmp edx, 0
   jl not_digit_x
   push rcx
   push rdx
   mov rcx, 10
   mul rcx
   pop rdx
   pop rcx
   add al, dl
   jmp fill_x
not_digit_x:
   add edx, '0'
   cmp edx, ' '
   je fill_x
   mov [x+4*rcx], eax
   inc rcx
   xor rax, rax
   jmp fill_x
end_x:
   xor rax, rax
   xor rcx, rcx
   xor rdx, rdx
fill_y:
   cmp rcx, ylen
   je end_y
   mov dl, [buffer+rbx]
   inc rbx
   sub edx, '0'
   cmp edx, 0
   jl not_digit_y
   push rcx
   push rdx
   mov rcx, 10
   mul rcx
   pop rdx
   pop rcx
   add al, dl
   jmp fill_y
not_digit_y:
   add edx, '0'
   cmp edx, ' '
   je fill_y
   mov [y+4*rcx], eax
   inc rcx
   xor rax, rax
   jmp fill_y
end_y:
   xor rax, rax
   xor rbx, rbx
   xor rcx, rcx
   xor rdx, rdx
sum:
   add eax, [x + 4*rbx]
   sub eax, [y + 4*rbx]
   inc rbx
   cmp rbx, xlen
   jne sum
average:
   cmp eax, 0
   jnl positive
   print char_minus, 1
   neg eax
   positive:
   mov rcx, xlen
   div rcx
   dprint
   cmp rdx, 0
   je end
   double_start:
   print char_point, 1
   xor rbx, rbx
   double:
   mov rcx, 10
   mov rax, rdx
   mul rcx
   mov rcx, xlen
   div rcx
   dprint
   inc rbx
   cmp rbx, 14
   je end
   cmp rdx, 0
   jne double
error:
    ; Exit with an error code
    mov rax, 1
    syscall
end:
   print newline, nlen
   print done, len
   print newline, nlen
   mov rax, 60
   xor rdi, rdi
   syscall

section .data
   char_minus db '-'
   char_point db '.'
   filename db 'data.txt', 0
   buffer times 1024 db 0
   x times 7 dd 0
   xlen equ (($ - x)/4)
   y times 7 dd 0
   ylen equ (($ - y)/4)

   done db 'Done', 0xA, 0xD
   len equ $ - done
   newline db 0xA, 0xD
   nlen equ $ - newline

section .bss
   result resb 1



