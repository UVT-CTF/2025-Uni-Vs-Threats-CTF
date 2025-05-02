#include <stdio.h>
#include<string.h>
#include<ctype.h>
#include<stdlib.h>
#include<stdint.h>
void flag(){
 printf("FAKE{fake_flags_are_friends_we_made_along_the_way}");
}

void configs(){
     int i, j, k;
    for (i = 0; i < 10; i++) {
        for (j = 0; j < 10; j++) {
            for (k = 0; k < 10; k++) {
                int fluff = i + j + k;
                fluff -= fluff;
            }
        }   
}
}

void verification(){
   char input[156]="asdwdwdeqwe";	
  char buffer[256];
    int i = 0, Flag = 0;
    
    while (input[i] && i < 255) {
        char c = input[i];

        if (isalpha(c)) {
            c ^= 0x20;
        }

        c = (c << 1) | (c >> 7);
        c ^= (i % 13);

        if ((c & 0x1F) == 0x1F) {
           Flag ^= 1;
        }

        buffer[i] = c;
        i++;
    }

    buffer[i] = '\0'; 

    for (int j = 0; j < i; j++) {
        char ch = buffer[j];

        ch = ~ch;
        ch &= 0xFF;
        ch ^= 0xAA;

        printf("%02X ", ch);

        if (((ch >> 3) & 1) == 1) {
           Flag = ~Flag;
        }
    }

}

static uint16_t module_init(uint8_t c)
{
    uint16_t t = (c ^ 0x83);
    t = ((t << 4) ^ 0x2A);
    t = ((t >> 8) | (t << 8)) & 0xFFFF;
    t ^= 0x3A29;
    return (t + 1440) & 0xFFFF;
}



void utilities(const char *src, uint16_t *dst)
{
    size_t i = 0;
    while (src[i])
    {
        dst[i] = module_init((uint8_t)src[i]);
        ++i;
    }
    dst[i] = 0;                
}



void initconfig(){
    const char q[] = "dF93aDNuX2R5c2tfMXNfbHkxbmc}";
    uint16_t enc[sizeof q] = {0};
    
    utilities(q, enc);
    puts(enc);
    uint16_t enc1[50];

    uint16_t ef[] = {0x75c4,0x45c4,0x65c4,0x95c6,0xf5c5,0x55c4,0x75c2,0x45c7,0x5c7,0x65c4,0xc5c5,0x65c6,0x5c7,0x15c2,0x85c5,0x75c2,0xa5c4,0x15c2,0x15c7,0x85c6,0xa5c4,0x15c2,0x5c4,0xb5c6,0x65c7,0xa5c4,0xf5c5};

    utilities(ef,enc1);

    puts(enc1);

}

