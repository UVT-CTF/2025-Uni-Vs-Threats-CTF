#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <time.h>

#define n 25
#define m 7
#define w 32
#define r 31
#define UMASK (0xffffffffUL << r)
#define LMASK (0xffffffffUL >> (w-r))
#define a 0x8EBFD028UL
#define u 11
#define s 7
#define t 15
#define l 18
#define b 0x2B5B2500UL
#define c 0xDB8B0000UL

typedef struct
{
    uint32_t state_array[n];
    int state_index;
} prng_state;


void initialize_state(prng_state* state, uint64_t seed) 
{
    uint32_t* state_array = &(state->state_array[0]);
    
    state_array[0] = seed;
    
    for (int i=1; i<n; i++)
    {
        seed ^= seed << 13;
        seed ^= seed >> 7;
        seed ^= seed << 17;
        state_array[i] = seed; 
    }
    
    state->state_index = 0;
}


uint32_t random_uint32(prng_state* state)
{
    uint32_t* state_array = &(state->state_array[0]);
    
    int k = state->state_index;

    int j = k - (n-1);
    if (j < 0) j += n;

    uint32_t x = (state_array[k] & UMASK) | (state_array[j] & LMASK);
    
    uint32_t xA = x >> 1;
    if (x & 0x00000001UL) xA ^= a;
    
    j = k - (n-m);
    if (j < 0) j += n;
    
    x = state_array[j] ^ xA;
    state_array[k++] = x;
    
    if (k >= n) k = 0;
    state->state_index = k;
    
    uint32_t y = x ^ (x >> u);
             y = y ^ ((y << s) & b);
             y = y ^ ((y << t) & c);
    uint32_t z = y ^ (y >> l);
    
    return z; 
}

uint8_t hex_to_byte(const char *hex) 
{
    uint8_t byte;
    sscanf(hex, "%2hhx", &byte);
    return byte;
}

void xor_with_prng(const uint8_t *data, size_t len, void *state) 
{
    for (size_t i = 0; i < len; i += 4) 
    {
        uint32_t rnd = random_uint32(state);
        for (int j = 0; j < 4 && (i + j) < len; j++) 
        {
            uint8_t xored = data[i + j] ^ ((rnd >> (8 * (3 - j))) & 0xFF);
            printf("%02x", xored);
        }
    }
    printf("\n");
}

void intro()
{
    printf("I built a one-time pad oracle! :)\n");
    printf("It's perfect! Nobody can decrypt anything without knowing the randomly generated numbers.\n");
    printf("That's why I have no problem tossing out encrypted secrets like this one: \n");
}

const char* FLAG = "UVT{prngs_4r3_v3ry_c00l}";
int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    prng_state state;
    uint64_t seed;

    memcpy(&seed, FLAG + 4, 8);
    seed += time(NULL);
    initialize_state(&state, seed);

    intro();
    xor_with_prng((const uint8_t *)FLAG, strlen(FLAG), &state);
    printf("\n");

    char hex_input[4096];

    while(1) {
        printf("Enter hex string: ");
        if (!fgets(hex_input, sizeof(hex_input), stdin)) 
        {
            fprintf(stderr, "Input error\n");
            return 1;
        }

        size_t hex_len = 0;
        for (size_t i = 0; hex_input[i]; i++) 
        {
            if (isspace((unsigned char)hex_input[i])) continue;

            if (!isxdigit((unsigned char)hex_input[i])) 
            {
                fprintf(stderr, "Invalid hex character: '%c'\n", hex_input[i]);
                return 1;
            }

            hex_input[hex_len++] = hex_input[i];
        }

        if (hex_len % 2 != 0) 
        {
            fprintf(stderr, "Hex input must have even number of digits\n");
            return 1;
        }

        size_t byte_len = hex_len / 2;
        uint8_t *data = malloc(byte_len);
        if (!data) 
        {
            perror("malloc");
            return 1;
        }

        for (size_t i = 0; i < byte_len; i++) 
        {
            data[i] = hex_to_byte(&hex_input[i * 2]);
        }

        xor_with_prng(data, byte_len, &state);
    }
}