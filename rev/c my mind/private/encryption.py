def criptare(c: int):
    t = c ^ 0x83
    t = (t << 4) & 0xFFFF  
    t ^= 0x2A
    t = ((t >> 8) | (t << 8)) & 0xFFFF     
    t ^= 0x3A29
    return (t + 1440) & 0xFFFF

def decriptare(a: int):
    a = (a - 1440) & 0xFFFF
    a ^= 0x3A29
    a = ((a >> 8) | (a << 8)) & 0xFFFF  
    a ^= 0x2A
    a = (a >> 4) & 0xFFFF  
    a ^= 0x83
    return a






decriptat = []
criptat = []

s = "UVT{MW5fbTNtb3J5X3czX3RydXM"

for ch in s:
    val = ord(ch)
    encrypted = criptare(val)
    decrypted = decriptare(encrypted)
    criptat.append(encrypted)
    decriptat.append(decrypted)

print("Encrypted:", criptat)
print("Decrypted:", decriptat)
print("Decrypted string:", ''.join(chr(c) for c in decriptat))

