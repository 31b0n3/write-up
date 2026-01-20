#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>
#include <unistd.h>


void init(){
    setvbuf(stdin, 0LL, 2, 0LL);
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stderr, 0LL, 2, 0LL);
}

int main()
{
    init();
    void (*code)(void) = mmap(0, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (code == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }
    fgets((char*)code, 0x1000, stdin);
    size_t len = strlen((char*)code);
    for(int i = 0 ; i < len; i++)
    {
        if(((uint16_t*)code)[i] == 0x0f05)
        {
            exit(0);
        }
    }
    close(0);
    close(1);
    close(2);
    code();
}
