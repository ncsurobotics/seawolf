#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BASE ((void*)0x20308000)
#define COUNT (16 * 1024)
#define WIDTH 32

int main(void) {
    unsigned short* n = malloc(sizeof(unsigned short) * COUNT);
    
    memcpy(n, BASE, sizeof(unsigned short) * COUNT);
    for(int i = 0; i < COUNT; i++) {
        if(i % WIDTH == 0) {
            printf("0x%04X\t\t", i);
        }
        printf("%04X ", n[i]);
        if((i + 1) % WIDTH == 0) {
            printf("\n");
        }
    }
    printf("\n");

    return 0;
}
