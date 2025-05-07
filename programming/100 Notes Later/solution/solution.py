from pwn import *

conn = remote("91.99.1.179", 60001)

notes = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5"]
notes.reverse()

note_lower_half = "\\__/"

cliff_size = 20

note_size = 10

conn.recvuntil(b"Press enter when you're ready!")
conn.send(b"\n")

for level in range(100):
    conn.recvline()
    conn.recvline()

    answer = [0] * 10
    for i in range(12):
        line = conn.recvline().decode()[:-1]
        print(line)
        for j in range(len(line)):
            if line[j] == "\\":
                if line[j:j+4] == note_lower_half:
                    answer[(j - cliff_size) // note_size] = notes[i]

    conn.sendline(" ".join(answer).encode())
    conn.recvline()

conn.interactive()