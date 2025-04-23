import random
import os

FLAG = os.environ['FLAG']

intro = """Oh, so you love music?
Name every note on this stave!
Read them. Recognize them. Write them out.
Talk music? Prove it.
"""

example = """                                  __
     /\\                          /  \\                            __                    |
 ____| |_________________________\\__/_________|_________________/  \\___________________|______ __ ________________________
|    |/        /                 |            |             |   \\__/                   |      /  \\   |      |       __
|____|_______ /_|________________|____________|______ __ ___|___|______________________|______\\__/___|______|______/  \\___
|   /|       /__|_      __       |            |      /  \\   |   |                      |      |      |      |      \\__/
|__/_|__________|______/  \\______|____________|______\\__/___|___|____________|______ __|______|______|______|______|______
| |  | _       /       \\__/      |          __|      |      |   |            |      /  \\      |      |      |      |
|_|__(,_)____ /_|______|_________|_________/  \\______|______|___|____________|______\\__/______|______|___ __|______|______
|  \\ | /     /__|_     |                   \\__/      |      |   |            |                |      |   /  \\      |
|____|__________|______|_____________________________|______|________________|________________|______|___\\__/______|______
     |                 |                             |                     __|                                     |
     |                 |                             |                   _/  \\_
   (_|                 |                                                  \\__/
Answer: B4 G5 G4 C5 F5 C4 A4 E5 F4 D5
NOTE: If the stave looks wrong, adjust your console dimensions to make it fit properly!!!
"""

wrong_answer = [
    "That's not even close. Are you sure you've seen a staff before?",
    "Be honest… did you just guess that one?",
    "You might wanna slow down and actually look at the notes.",
    "It's okay, not everyone's born with perfect pitch... or eyesight.",
    "Oops. That note was off-key, just like your answer.",
    "Somewhere, a music teacher just cried.",
    "Wrong again. But hey, you're consistent!",
    "Did you even try with that one?"
]

right_answer = [
    "Good.",
    "Keep going!",
    "You're right. I guess miracles do happen.",
    "Lucky guess? No? Hmph. Alright then.",
    "Not bad… for now.",
    "Yeah, yeah, you got it. Don't get cocky.",
    "Ugh. I guess you do know a little something.",
    "Whatever. Even a broken clock is right twice a day."
]

NOTE = {
    "C4": 12,
    "D4": 11,
    "E4": 10, 
    "F4": 9,
    "G4": 8, 
    "A4": 7, 
    "B4": 6, 
    "C5": 5, 
    "D5": 4, 
    "E5": 3, 
    "F5": 2, 
    "G5": 1
}

CLEF = """                    
     /\\             
 ____| |____________
|    |/        /    
|____|_______ /_|___
|   /|       /__|_  
|__/_|__________|___
| |  | _       /    
|_|__(,_)____ /_|___
|  \\ | /     /__|_  
|____|__________|___
     |              
     |              
   (_|              """

NOTE_ON_LINE = """  __  
_/  \\_
 \\__/ """

NOTE_BETWEEN_LINES = """ __ 
/  \\
\\__/"""


def crateStaff():
    return [[] for _ in range(14)]


def drawClef(staff):
    clef = CLEF.split("\n")

    for i in range(14):
        staff[i] += [c for c in clef[i]]

    return staff


def drawNote(staff, note):
    on_line = ["C4", "E4", "G4", "B4", "D5", "F5"]
    between_lines = ["D4", "F4", "A4", "C5", "E5", "G5"]

    pos = NOTE[note]
    staff[0] += [" "] * 10

    for i in range(1, 12):
        if i % 2 == 1:
            staff[i] += [" "] * 10
        else:
            staff[i] += ["_"] * 10

    for i in range(12, 14):
        staff[i] += ([" "] * 10)

    if note in on_line:
        note_drawing = NOTE_ON_LINE.split("\n")
        for i in range(pos - 1, pos + 2):
            for j in range(6):
                staff[i][-8 + j] = note_drawing[i - pos + 1][j]
    elif note in between_lines:
        note_drawing = NOTE_BETWEEN_LINES.split("\n")
        for i in range(pos - 1, pos + 2):
            for j in range(4):
                staff[i][-7 + j] = note_drawing[i - pos + 1][j]

    if pos < 7:
        for i in range(6):
            staff[pos + i + 2][-7] = '|'
    else:
        for i in range(6):
            staff[pos - i - 1][-4] = '|'

    return staff

def drawBarLine(staff):
    staff[0] += " "
    staff[1] += " "
    staff[2] += "_"
    for i in range(3, 11):
        staff[i] += "|"

    staff[11] += " "
    staff[12] += " "
    staff[13] += " "

    return staff

    
def printStaff(staff):
    for line in staff:
        print("".join(line))

print(intro)
print("Here's an example: ")
print(example)

input("Press enter when you're ready!")

notes = list(NOTE.keys())

for level in range(100):
    random_notes = [random.choice(notes) for _ in range(10)]

    staff = crateStaff()
    staff = drawClef(staff)

    for i in range(10):
        if i % 4 == 0 and i != 0:
            drawBarLine(staff)
        drawNote(staff, random_notes[i])

    printStaff(staff)
    # print(" ".join(random_notes))

    answer = input("Answer: ").split(" ")

    if answer == random_notes:
        print(random.choice(right_answer))
    else:
        print(random.choice(wrong_answer))
        exit()

print("\n")
print("Huh! You actualy know!")
print("Here, you deserve it...")
print(FLAG)