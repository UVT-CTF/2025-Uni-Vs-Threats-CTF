values = [0x127, 0x124, 0x122, 0x155, 0xd8, 0xbb, 0x10d, 0x165, 0x101, 0xd8,
    0xb6, 0xbb, 0xbb, 0x163, 0x16c, 0xf9, 0x101, 0xbd, 0x124, 0xbd,
    0x178, 0x153, 0xb6, 0x16c, 0x117, 0x101, 0xbb, 0x87, 0x101, 0x16f,
    0x153, 0x101, 0x11e, 0xb6, 0x108, 0x108, 0x133, 0x15f]

flag = ""
for el in values:
    flag += chr(((el ^ 0x23) + 40) // 3 - 15)

print(flag)
