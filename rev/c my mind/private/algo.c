#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

#define SIZE 4
#define BLOCK_SIZE 16

#define BOGUS_LOOP for (int __bogus = 0; __bogus < 1; __bogus++) if (__bogus == 999) continue;

volatile int confuse = 0;
int skip_row, skip_col; // Store skip positions for decryption

void imul(char mat[SIZE][SIZE], int skiprow, int skipcol) {
    BOGUS_LOOP
    int distraction = (int)(time(NULL) % 1337);
    volatile int ghost = distraction * 42;

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            int shadow = (i ^ j) + (ghost & 0xFF);
            shadow ^= 0xDE;
            if (!(i == skiprow && j == skipcol)) {
                mat[i][j] <<= 1; // Bit shift (reversible)
                confuse += mat[i][j] ^ shadow;
            } else {
                confuse ^= (mat[i][j] + 91);
            }
        }
    }
}

void imul_reverse(char mat[SIZE][SIZE], int skiprow, int skipcol) {
    BOGUS_LOOP
    volatile char dummy = 'z';
    dummy ^= 0x3F;
    confuse |= dummy;

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (!(i == skiprow && j == skipcol)) {
                mat[i][j] >>= 1; // Reverse bit shift
            }
        }
    }
}

void add(char mat[SIZE][SIZE], int skiprow, int skipcol) {
    BOGUS_LOOP
    volatile uint32_t hashNoise = 0xABADBABE;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            int junk = (i * j) ^ (hashNoise >> 3);
            if (!(i == skiprow && j == skipcol)) {
                mat[i][j] += 51;
                confuse ^= junk;
            }
        }
    }
}

void add_reverse(char mat[SIZE][SIZE], int skiprow, int skipcol) {
    BOGUS_LOOP
    int confusionBuffer[4] = {1337, 42, 666, 9001};
    for (int x = 0; x < 4; x++) confusionBuffer[x] ^= x * 3;

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (!(i == skiprow && j == skipcol)) {
                mat[i][j] -= 51;
            }
        }
    }
}

void xori(char mat[SIZE][SIZE], int skiprow, int skipcol) {
    volatile int seed = 123456;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            seed ^= (i << j);
            if (!(i == skiprow && j == skipcol)) {
                mat[i][j] ^= 0x3A;
                if ((mat[i][j] & 0xF0) == 0xA0) {
                    confuse += seed; // fake condition trap
                }
            }
        }
    }
}

void transposeUpToChar(char matrix[SIZE][SIZE], int rows, int cols, char stopChar, int stopRow, int stopCol) {
    volatile int fakeFlag = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = i + 1; j < cols; j++) {
            if ((i == stopRow && j == stopCol) || (j == stopRow && i == stopCol)) {
                if ((matrix[i][j] ^ matrix[j][i]) == (stopChar ^ 0x5A)) {
                    puts("Transmission abort condition met.");
                    fakeFlag ^= 1;
                    goto skip_transpose;
                }
            }

            char shadow = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = shadow;

            confuse += shadow ^ (i << 4) ^ (j << 2);
        }
    }

skip_transpose:
    if (fakeFlag && confuse % 2 == 0) {
        puts("Stalling decryptor...");
        for (volatile int i = 0; i < 1000000; i++); // delay loop
    }
}

int check(char matrix[SIZE][SIZE]) {
    int randFill = rand() % 1000;
    confuse ^= randFill;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (matrix[i][j] == '0') {
                skip_row = i; // Store skip positions
                skip_col = j;
                return i * 10 + j;
            }
        }
    }
    skip_row = 2; // Default if '0' not found
    skip_col = 2;
    return 22;
}

void encrypt(char matrix[SIZE][SIZE]) {
    int coord = check(matrix);
    transposeUpToChar(matrix, SIZE, SIZE, '0', skip_row, skip_col);
    imul(matrix, skip_row, skip_col);
    add(matrix, skip_row, skip_col);
    xori(matrix, skip_row, skip_col);
    confuse ^= matrix[0][0]; // decoy
}

void decrypt(char matrix[SIZE][SIZE]) {
    xori(matrix, skip_row, skip_col);
    add_reverse(matrix, skip_row, skip_col);
    imul_reverse(matrix, skip_row, skip_col);
    transposeUpToChar(matrix, SIZE, SIZE, '0', skip_row, skip_col); // Reverse transpose
    confuse += matrix[3][3]; // decoy
}

void printHex(char* data, int len) {
    for (int i = 0; i < len; i++)
        printf("%02X ", (unsigned char)data[i]);
    printf("\n");
}

int main() {
    srand(time(NULL));

    char input[BLOCK_SIZE + 1] = "3245894954829435"; 
    char encrypted[BLOCK_SIZE];
    char decrypted[BLOCK_SIZE];
    char matrix[SIZE][SIZE];

    printf("Original: %s\n", input);

    // Encrypt
    for (int i = 0; i < BLOCK_SIZE; i++)
        matrix[i / SIZE][i % SIZE] = input[i];
    encrypt(matrix);
    for (int i = 0; i < BLOCK_SIZE; i++)
        encrypted[i] = matrix[i / SIZE][i % SIZE];
    printf("Encrypted (hex): ");
    printHex(encrypted, BLOCK_SIZE);

    // Decrypt
    for (int i = 0; i < BLOCK_SIZE; i++)
        matrix[i / SIZE][i % SIZE] = encrypted[i];
    decrypt(matrix);
    for (int i = 0; i < BLOCK_SIZE; i++)
        decrypted[i] = matrix[i / SIZE][i % SIZE];
    decrypted[BLOCK_SIZE] = '\0';
    printf("Decrypted: %s\n", decrypted);

    return 0;
}
