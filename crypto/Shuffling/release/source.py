#!/usr/local/bin/python3
import random
import time

FLAG = "UVT{F4k3_fl4g}"
P = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]

def padd(l):
    random.seed(int(time.time()))
    for _ in range(32 - len(l)):
        l.append(random.randint(32, 125))
    
    return l


def shuffle(l):
    nl = []
    for p in P:
        nl.append(l[p])

    return nl


def encrypt(pt):
    l = [ord(x) for x in pt]
    l = padd(l)
    l = shuffle(l)

    random.seed(sum(l))
    key = random.randbytes(len(l))

    ct = [x ^ y for x, y in zip(l, key)]

    return bytes(ct)

print(encrypt(FLAG).hex())