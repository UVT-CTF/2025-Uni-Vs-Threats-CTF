#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <dlfcn.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/syscall.h>
#include <stdlib.h>
#include <stdint.h>
#include <openssl/aes.h>
#include "encrypted.h"
#include "junk.h"
#ifndef SYS_memfd_create
#define SYS_memfd_create 319
#endif

#ifndef MFD_CLOEXEC
#define MFD_CLOEXEC 0x0001
#endif

void print_hex(const unsigned char* data, int len) {
    for (int i = 0; i < len; ++i) {
        printf("%02x", data[i]);
        if ((i + 1) % 16 == 0) printf("\n");
    }
    printf("\n");
}

void write_binary(const char* filename, unsigned char* data, int len) {
    FILE* file = fopen(filename, "wb");
    if (!file) {
        perror("Failed to open file");
        return;
    }
    fwrite(data, 1, len, file);
    fclose(file);
}

void aes_encrypt_cbc(const unsigned char *plaintext, int pt_len,
                     const unsigned char *key, const unsigned char *iv,
                     unsigned char *ciphertext) {
    AES_KEY aes_key;
    AES_set_encrypt_key(key, 128, &aes_key);
    AES_cbc_encrypt(plaintext, ciphertext, pt_len, &aes_key, (unsigned char *)iv, AES_ENCRYPT);
}

void aes_decrypt_cbc(const unsigned char *ciphertext, int ct_len,
                     const unsigned char *key, const unsigned char *iv,
                     unsigned char *plaintext) {
    AES_KEY aes_key;
    AES_set_decrypt_key(key, 128, &aes_key);
    AES_cbc_encrypt(ciphertext, plaintext, ct_len, &aes_key, (unsigned char *)iv, AES_DECRYPT);
}

void aes_encrypt() {
    unsigned char key[16] = "1234456781234568";
    unsigned char iv[16] = "1234567812345678";

    int padded_len = ((junk_so_len + AES_BLOCK_SIZE - 1) / AES_BLOCK_SIZE) * AES_BLOCK_SIZE;
    unsigned char plaintext[padded_len];
    memcpy(plaintext, junk_so, junk_so_len);

    unsigned char pad_value = padded_len - junk_so_len;
    memset(plaintext + junk_so_len, pad_value, pad_value);

    unsigned char ciphertext[padded_len];
    aes_encrypt_cbc(plaintext, padded_len, key, iv, ciphertext);

    printf("Original data (%d bytes):\n", junk_so_len);
    print_hex(junk_so, junk_so_len);

    printf("\nEncrypted data (%d bytes):\n", padded_len);
    print_hex(ciphertext, padded_len);

    write_binary("encrypted.bin", ciphertext, padded_len);

    // Decrypt
    unsigned char decrypted[padded_len];
    memcpy(iv, "1234567812345678", 16);  // Reset IV
    aes_decrypt_cbc(ciphertext, padded_len, key, iv, decrypted);

    int decrypted_len = padded_len - decrypted[padded_len - 1];

    printf("\nDecrypted data (%d bytes):\n", decrypted_len);
    print_hex(decrypted, decrypted_len);

    write_binary("decrypted.bin", decrypted, decrypted_len);
}

void decryptiv(int mat[4][4]) {
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            mat[i][j] >>= 1;
}

void encryptiv(int mat[4][4]) {
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            mat[i][j] <<= 1;
}


int main() {
    puts("I found something interesting you may want to look at it");
  
    puts("But be careful, it is unstable and can crash if left uncontrolled");
   
    int fd = syscall(SYS_memfd_create, "mylib", MFD_CLOEXEC);
    if (fd == -1) {
        perror("memfd_create");
        return 1;
    }

    if (write(fd, encrypted_bin, encrypted_bin_len) != encrypted_bin_len) {
        perror("write");
        close(fd);
        return 1;
    }

    char path[64];
    snprintf(path, sizeof(path), "/proc/self/fd/%d", fd);

    void *handle = dlopen(path, RTLD_LAZY);
    if (!handle) {
        fprintf(stderr, "dlopen failed: %s\n", dlerror());
        close(fd);
        return 1;
    }

    int fakekey[16] = {1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8};
    int fakeiv[16]  = {1,2,3,4,4,6,7,8,1,2,3,4,5,6,7,8};
    int matrixkey[4][4], matrixiv[4][4];

    for (int i = 0, k = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            matrixkey[i][j] = fakekey[k++];

    for (int i = 0, k = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            matrixiv[i][j] = fakeiv[k++];

    encryptmat(matrixkey);
    encryptiv(matrixiv);

    int key_decrypt[16] = {1,2,4,2,3,4,4,2,3,2,4,3,2,3,4,3};
    int iv_decrypt[16]  = {8,9,2,3,4,7,9,4,4,7,7,8,8,7,4,9};

    aes_encrypt();

    void (*flag)() = dlsym(handle, "flag");
    if (!flag) {
        fprintf(stderr, "dlsym failed: %s\n", dlerror());
        dlclose(handle);
        close(fd);
        return 1;
    }

    flag();  
    dlclose(handle);
    close(fd);
    return 0;
}

