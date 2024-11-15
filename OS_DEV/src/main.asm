org 0x7C00
bits 16

%define ENDL 0x0D, 0x0A ; Nasm Macro for new line
start:
    jmp main

; Prints a string to the screen
; Params:
; - ds:si points to string
puts:
    ; save registers we will modify
    push si
    push ax

.loop:
    lodsb ; loads next character in al
    or al,al ; verify if next char is null?
    jz .done

    mov ah, 0x0e ; calls bios interrupt
    mov bh,0
    int 0x10
    jmp .loop
.done:
    pop ax
    pop si
    ret

main:
    ; setting up data segments
    mov ax,0 ; Since we can't directly to ds/es
    mov ds,ax
    mov es,ax

    ; setting up the stack
    mov ss,ax
    mov sp,0x7c00 ; stack goes downwards from where we loaded it to the memory

    ; print message
    mov si, msg_hello
    call puts

    hlt
.halt:
    jmp .halt

msg_hello : db 'Happy Birthday Shadz!', ENDL, 0

times 510-($-$$) db 0
dw 0AA55h
