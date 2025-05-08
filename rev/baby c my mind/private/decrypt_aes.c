#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <openssl/aes.h>
#include "encrypted.h"

void write_binary(const char* filename, unsigned char* data, int len) {
    FILE* file = fopen(filename, "wb"); 
    fwrite(data, 1, len, file);
    fclose(file);
}

void aes_decrypt_cbc(const unsigned char *ciphertext, int ct_len,
                    const unsigned char *key, const unsigned char *iv,
                    unsigned char *plaintext) {
    AES_KEY aes_key;
    AES_set_decrypt_key(key, 128, &aes_key);
    AES_cbc_encrypt(ciphertext, plaintext, ct_len, &aes_key, (unsigned char *)iv, AES_DECRYPT);
}

void print_hex(const unsigned char *data, int len) {
    for (int i = 0; i < len; i++) {
        printf("%02x ", data[i]);
    }
    printf("\n");
}

int main() {
    unsigned char key[16] = "";
    unsigned char iv[16] = "";
    
    int padded_len = ((encrypted_so_len + AES_BLOCK_SIZE - 1) / AES_BLOCK_SIZE) * AES_BLOCK_SIZE;
    unsigned char decrypted[padded_len];
    
    aes_decrypt_cbc(encrypted_so, padded_len, key, iv, decrypted);
    
    int decrypted_len = padded_len;
    unsigned char pad_value = decrypted[padded_len - 1];
    if (pad_value <= AES_BLOCK_SIZE) {
        decrypted_len -= pad_value;
    }
    
    printf("\nDecrypted data (%d bytes):\n", decrypted_len);
    print_hex(decrypted, decrypted_len);
    write_binary("decrypted.bin",decrypted,decrypted_len);    
    return 0;
}

