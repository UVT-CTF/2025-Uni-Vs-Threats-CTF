import random
from pwn import *

P = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]

def is_printable(pt):
    for x in pt:
        if x < 32 or x > 128:
            return False
        
    return True

def unshuffle(pt):
    result = [0] * 32
    for i in range(32):
        result[P[i]] = pt[i]

    return bytes(result)


ct = "d1b573c954cbf61815ae3ab555f6903a2696393ead3d279d7d213e152a3fdea6"
ct = bytes.fromhex(ct)

for i in range(1024, 4096):
    random.seed(i)
    key = random.randbytes(32)

    pt = xor(ct, key)

    if is_printable(pt):
        break

print(pt)

pt = unshuffle(pt)
print(pt)