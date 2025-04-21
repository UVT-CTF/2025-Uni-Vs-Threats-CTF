#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define TARGET_LEN 43

// XOR key cycling through "U", "V", "T"
const char xor_key[3] = { 'U', 'V', 'T' };


// Target XOR result
const unsigned char target[TARGET_LEN] = {
    0x3d, 0x22, 0x20, 0x25, 0x25, 0x6e, 0x7a, 0x79, 0x23, 0x22,
    0x21, 0x7a, 0x2c, 0x39, 0x21, 0x21, 0x23, 0x36, 0x30, 0x78,
    0x37, 0x3a, 0x3b, 0x7b, 0x22, 0x37, 0x20, 0x36, 0x3e, 0x6b,
    0x23, 0x6b, 0x30, 0x04, 0x21, 0x60, 0x22, 0x6f, 0x03, 0x32,
    0x0e, 0x37, 0x04
};

const int alt_target[] = {
    0x127, 0x124, 0x122, 0x155, 0xd8, 0xbb, 0x10d, 0x165, 0x101, 0xd8,
    0xb6, 0xbb, 0xbb, 0x163, 0x16c, 0xf9, 0x101, 0xbd, 0x124, 0xbd,
    0x178, 0x153, 0xb6, 0x16c, 0x117, 0x101, 0xbb, 0x87, 0x101, 0x16f,
    0x153, 0x101, 0x11e, 0xb6, 0x108, 0x108, 0x133, 0x15f
};

void check_flag() {
    char input[100];
    printf("Enter secret key: ");
    if (fgets(input, sizeof(input), stdin) == NULL) {
        fprintf(stderr, "Failed to read input.\n");
        exit(1);
    }

    input[strcspn(input, "\n")] = 0;
    size_t len = strlen(input);


    for (size_t i = 0; i < TARGET_LEN; i++) {
        int computed = ((input[i] + 15) * 3 - 40) ^ 0x23;
        if (computed != alt_target[i]) {
            fprintf(stderr, "Still cannot get it? Shame on you!\n");
            exit(1);
        }
    }

    printf("Finally! Congrats! Now go solve something else, I've got things to do!\n");
}

int main() {
    char input[100];

    printf("Enter my secret: ");
    if (fgets(input, sizeof(input), stdin) == NULL) {
        fprintf(stderr, "Error reading input.\n");
        return 1;
    }

    // Remove trailing newline
    input[strcspn(input, "\n")] = 0;

    size_t len = strlen(input);

    if (len != TARGET_LEN) {
        fprintf(stderr, "Invalid input length!\n");
        return 1;
    }

    for (size_t i = 0; i < TARGET_LEN; i++) {
        char key_char = xor_key[i % 3];
        if ((input[i] ^ key_char) != target[i]) {
            fprintf(stderr, "NONONO! GET OUT OF HERE! ABORT! ABORT!\n");
            return 1;
        }
    }

    printf("YOU'RE RIGHT! BUT YOU'RE STILL WRONG! XD\n");
    return 0;
}


// ((input[i] + 15) * 3 - 40) ^ 0x23 
// UVT{R1ck_R011inG_3V3ry0ne_15_my_h0bbY}
