import math

def to_signed(n):
    return n - 0x100000000 if n & 0x80000000 else n

def js_remainder(a, b):
    return a - b * math.trunc(a / b)

# https://gist.github.com/tommyettinger/46a874533244883189143505d203312c
def next_rand(seed):
    seed = (seed + 0x9e3779b9) & 0xFFFFFFFF
    seed ^= seed >> 16
    seed = (seed * 0x21f0aaad) & 0xFFFFFFFF  # Math.imul
    seed ^= seed >> 15
    seed = (seed * 0x735a2d97) & 0xFFFFFFFF  # Math.imul
    seed ^= seed >> 15
    return seed

def decrypt_flag(encrypted_flag):
    flag = encrypted_flag.copy()
    N = len(flag)

    seed = 0xDEADBEEF & 0xFFFFFFFF
    
    operations = []
    
    for L in range(N - 1, 0, -1):
        i = L + 1
        
        seed = next_rand(seed)
        r1 = seed
        signed_r1 = to_signed(r1)
        remainder = js_remainder(signed_r1, i)
        shuffle_pos = abs(remainder)

        seed = next_rand(seed)
        r2 = seed
        key = r2 >> 2
        operations.append((L, shuffle_pos, key))
    
    for L, shuffle_pos, key in reversed(operations):
        flag[L] = (flag[L] ^ key) & 0xFF
        flag[L], flag[shuffle_pos] = flag[shuffle_pos], flag[L]
    
    return flag

encrypted_flag = [
    48,32,83,245,235,124,151,6,39,92,222,143,240,123,151,155,39,242,236,47,13
]

decrypted = decrypt_flag(encrypted_flag)
print("".join(chr(x) for x in decrypted))  
