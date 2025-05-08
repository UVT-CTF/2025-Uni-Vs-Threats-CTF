
#include "./include/utils.h"

void readline(char* buff)
{
    char scratch_buffer[64] = {0};
    
    while(1){
        read(0, scratch_buffer, 64);
        for(unsigned int i = 0; i < 64; ++i){
            if(scratch_buffer[i] == '\n')
                goto done;
            *buff = scratch_buffer[i];
            ++buff;
        }
    }
done:
    *buff = '\0';
}

void printline(char* buffer)
{
    write(1, buffer, stringlen(buffer));
    write(1, "\n", 1);
}

int stringlen(char* string)
{
    int size = 1; 

    while(*string != '\0'){
        ++size;
        ++string;
    }

    return size;
}

__attribute__((noreturn)) 
void exit(int exitCode)
{
    register long param1 asm ("edi") = exitCode;

    (void)param1;

    __asm__(
        "mov eax, 0x3c\n"
        "syscall\n"
        : 
        : "r" (exitCode)
        : "eax", "rdi"
    );
    __builtin_unreachable();
}