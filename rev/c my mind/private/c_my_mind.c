#define _GNU_SOURCE
#include <openssl/aes.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <dlfcn.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/syscall.h>
#include "encrypted.h"  
#include <time.h>
#include <stdlib.h>
#include <stdint.h>

#ifndef MFD_CLOEXEC
#define MFD_CLOEXEC 0x0001U
#endif

#define SIZE 4
#define BLOCK_SIZE 16

#define BOGUS_LOOP for (int __bogus = 0; __bogus < 1; __bogus++) if (__bogus == 999) continue;

volatile int g = 0;
int skip_row, skip_col;

extern unsigned char file_so[];  extern size_t file_so_len;      
void aes_encrypt_cbc(const unsigned char *plaintext, int pt_len,
                      const unsigned char *key, const unsigned char *iv,
                      unsigned char *ciphertext) {
    AES_KEY aes_key;
    AES_set_encrypt_key(key, 128, &aes_key);
    AES_cbc_encrypt(plaintext, ciphertext, pt_len, &aes_key, (unsigned char *)iv, AES_ENCRYPT);
}

void abcf(char mat[SIZE][SIZE], int skiprow, int skipcol) {
      volatile uint16_t sdc[8] = {0xa1, 0xa1, 0x38, 0xa3, 0xa7, 0x9f,0xad,0xa7};
    volatile uint16_t sum = 0;
for (int x = 0; x < 8; x++) {
    sum += sdc[x];
} 

 
   BOGUS_LOOP
    int pointer = (int)(time(NULL) % 1337);
    volatile int ghost = pointer * 42;

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            int shadow = (i ^ j) + (ghost & 0xFF);
            shadow ^= 0xDE;
            if (!(i == skiprow && j == skipcol)) {
                mat[i][j] <<= 1;
                g += mat[i][j] ^ shadow;
            } else {
                g ^= (mat[i][j] + 91);
            }
        }
    }
}

void deadeads(char mat[SIZE][SIZE], int skiprow, int skipcol) {
    BOGUS_LOOP
       volatile uint16_t op[8] = {0xa1, 0xa7, 0xa7, 0xa5, 0xa7, 0xa3, 0xa1, 0x9b};
    volatile uint16_t sum = 0;
for (int x = 0; x < 8; x++) {
    sum += op[x];
}	    


    volatile uint32_t hashNoise = 0x45a9;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            int junk = (i * j) ^ (hashNoise >> 3);
            if (!(i == skiprow && j == skipcol)) {
                mat[i][j] += 51;
                g ^= junk;
            }
        }
    }
}

void rrgter(char mat[SIZE][SIZE], int skiprow, int skipcol) {
    volatile uint16_t sde[8] = {0xa1, 0x99, 0x33, 0xa1, 0x9b,0x9b, 0xa1, 0xa1};
    volatile int sum=0;
    for (int x = 0; x < 8; x++) {
    sum += sde[x];
}
    


    volatile int seed = 453783;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            seed ^= (i << j);
            if (!(i == skiprow && j == skipcol)) {
                mat[i][j] ^= 0x3A;
                if ((mat[i][j] & 0xF0) == 0xA0) {
                    g += seed;
                }
            }
        }
    }
}

void asdsdewrf(char matrix[SIZE][SIZE], int rows, int cols, char stopChar, int stopRow, int stopCol) {
    volatile  uint16_t daas[8] = {[0]=0xa3, [1]=0x99, [2]=0xa7, [3]=0x9f, [4]=0xad, [5]=0x9f, [6]=0xa1, [7]=0xa1};
       volatile uint16_t sum = 0;
    for (int x = 0; x < 8; x++) {
        sum += daas[x];
   }



    volatile int Flag = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = i + 1; j < cols; j++) {
            if ((i == stopRow && j == stopCol) || (j == stopRow && i == stopCol)) {
                if ((matrix[i][j] ^ matrix[j][i]) == (stopChar ^ 0x5A)) {
                    puts("unable to find the byte");
                    Flag ^= 1;
                    goto skip_transpose;
                }
            }

            char shadow = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = shadow;

            g += shadow ^ (i << 4) ^ (j << 2);
        }
    }

skip_transpose:
    if (Flag && g % 2 == 0) {
        puts("iterate through bits");
        for (volatile int i = 0; i < 1000000; i++);
    }
}

int defg(char matrix[SIZE][SIZE]) {
    int randFill = rand() % 1000;
    g ^= randFill;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (matrix[i][j] == '0') {
                skip_row = i;
                skip_col = j;
                return i * 10 + j;
            }
        }
    }
    skip_row = 2;
    skip_col = 2;
    return 22;
}

void encrypt(char matrix[SIZE][SIZE]) {
    int coord = defg(matrix);
    asdsdewrf(matrix, SIZE, SIZE, '0', skip_row, skip_col);
    abcf(matrix, skip_row, skip_col);
    deadeads(matrix, skip_row, skip_col);
    rrgter(matrix, skip_row, skip_col);
    g ^= matrix[0][0];
    int state = 0;
    while (1) {
        int a = 0;          switch (state) {
            case 0:
                a += 3;
                state = 1;
                break;
            case 1:
                a *= 2;
                state = 2;
                break;
            case 2:
                return;
        }
    }
}

int main() {
    puts("Wait i have something for you!\n");

    int fd = syscall(SYS_memfd_create, "mylib", MFD_CLOEXEC);
    if (fd == -1) {
        perror("memfd_create");
        return 1;
    }

    if (write(fd, encrypted_bin, encrypted_bin_len) != encrypted_bin_len) {
        perror("write");
        return 1;
    }

    char path[64];
    snprintf(path, sizeof(path), "/proc/self/fd/%d", fd);
    void *handle = dlopen(path, RTLD_LAZY);  
    if(!handle){
      puts( "Oh no i lost it :(("); 
      puts("But i still remember how it looks");
      puts("I'm going to say it quick before the null pointer finds me, had a size of 4 and a length of 128 and a.......");	
    }
    dlclose(handle);
    unsigned char key[16] = "clearlythisisthe";
    unsigned char iv[16] = "keythatyousearch";
    unsigned char plaintext[32] = "btw i use arch";
    unsigned char ciphertext[32];
    aes_encrypt_cbc(plaintext, sizeof(plaintext), key, iv, ciphertext);

    unsigned char input[BLOCK_SIZE] = "inputdata";
    char sdsfsr[SIZE][SIZE];
    for (int i = 0; i < BLOCK_SIZE; i++)
        sdsfsr[i / SIZE][i % SIZE] = input[i];
    encrypt(sdsfsr);
    defg(sdsfsr);
}

