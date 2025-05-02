#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <openssl/aes.h>

// Include the header file containing the data array and length
#include "shield.h"  // Replace with your actual .h filename

// Fixed write_binary function
void write_binary(const char* filename, unsigned char* data, int len) {
    FILE* file = fopen(filename, "wb");
    if(!file) {
        perror("Failed to open file");
        return;
    }
    fwrite(data, 1, len, file);  // Fixed: Added len parameter
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

void print_hex(const unsigned char *data, int len) {
    for (int i = 0; i < len; i++) {
        printf("%02x ", data[i]);
    }
    printf("\n");
}

int main() {
    unsigned char key[16] = "3245894954829435";
    unsigned char iv[16] = "4547538754346744";
    
    // Calculate padded length
    int padded_len = ((shield_so_len + AES_BLOCK_SIZE - 1) / AES_BLOCK_SIZE) * AES_BLOCK_SIZE;
    
    // Allocate and pad plaintext
    unsigned char plaintext[padded_len];
    memcpy(plaintext, shield_so, shield_so_len);
    
    // Apply PKCS#7 padding if needed
    if (shield_so_len % AES_BLOCK_SIZE != 0) {
        unsigned char pad_value = AES_BLOCK_SIZE - (shield_so_len % AES_BLOCK_SIZE);
        memset(plaintext + shield_so_len, pad_value, pad_value);
    }
    
    // Allocate space for ciphertext
    unsigned char ciphertext[padded_len];
    
    // Encrypt the data
    aes_encrypt_cbc(plaintext, padded_len, key, iv, ciphertext);
    
    printf("Original data (%d bytes):\n", shield_so_len);
    print_hex(shield_so, shield_so_len);
    
    printf("\nEncrypted data (%d bytes):\n", padded_len);
    print_hex(ciphertext, padded_len);
    
    // Write encrypted data to file (fixed variable name)
    write_binary("encrypted.bin", ciphertext, padded_len);
    
    // Decrypt to verify
    unsigned char decrypted[padded_len];
    memcpy(iv, "4547538754346744", 16); // Reset IV
    aes_decrypt_cbc(ciphertext, padded_len, key, iv, decrypted);
    
    // Remove padding
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
