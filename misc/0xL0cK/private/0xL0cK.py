import os
import sys
import time
import random
from colorama import init, Fore, Style


# Password system variables
PASSWORDS = ["SURVIVOR", "PROTOCOL", "MIRROR", "REACTOR", "INFINITY", "GATEWAY"]
CORRECT_PASSWORD = random.choice(PASSWORDS)
JUNK_CHARS = "!@#$%^&*()_+-=[]{}|;:',.<>?/"
password_timeout = 0
password_address = ""
attempts = 4
attempts_admin = 2

# Terminal state
unlocked = False
unlocked_admin = False
session_start = time.time()

def type_out(text, delay=0.03):  # You can tweak the delay
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Style.RESET_ALL + "\n")  # Reset colors and move to next line
    sys.stdout.flush()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def terminal_header():
    print(Fore.GREEN + Style.BRIGHT + r"""
                                                                                                                           
                                                                                                                           
     000000000                         LLLLLLLLLLL                  OOOOOOOOO             CCCCCCCCCCCCCKKKKKKKKK    KKKKKKK
   00:::::::::00                       L:::::::::L                OO:::::::::OO        CCC::::::::::::CK:::::::K    K:::::K
 00:::::::::::::00                     L:::::::::L              OO:::::::::::::OO    CC:::::::::::::::CK:::::::K    K:::::K
0:::::::000:::::::0                    LL:::::::LL             O:::::::OOO:::::::O  C:::::CCCCCCCC::::CK:::::::K   K::::::K
0::::::0   0::::::0xxxxxxx      xxxxxxx  L:::::L               O::::::O   O::::::O C:::::C       CCCCCCKK::::::K  K:::::KKK
0:::::0     0:::::0 x:::::x    x:::::x   L:::::L               O:::::O     O:::::OC:::::C                K:::::K K:::::K   
0:::::0     0:::::0  x:::::x  x:::::x    L:::::L               O:::::O     O:::::OC:::::C                K::::::K:::::K    
0:::::0 000 0:::::0   x:::::xx:::::x     L:::::L               O:::::O     O:::::OC:::::C                K:::::::::::K     
0:::::0 000 0:::::0    x::::::::::x      L:::::L               O:::::O     O:::::OC:::::C                K:::::::::::K     
0:::::0     0:::::0     x::::::::x       L:::::L               O:::::O     O:::::OC:::::C                K::::::K:::::K    
0:::::0     0:::::0     x::::::::x       L:::::L               O:::::O     O:::::OC:::::C                K:::::K K:::::K   
0::::::0   0::::::0    x::::::::::x      L:::::L         LLLLLLO::::::O   O::::::O C:::::C       CCCCCCKK::::::K  K:::::KKK
0:::::::000:::::::0   x:::::xx:::::x   LL:::::::LLLLLLLLL:::::LO:::::::OOO:::::::O  C:::::CCCCCCCC::::CK:::::::K   K::::::K
 00:::::::::::::00   x:::::x  x:::::x  L::::::::::::::::::::::L OO:::::::::::::OO    CC:::::::::::::::CK:::::::K    K:::::K
   00:::::::::00    x:::::x    x:::::x L::::::::::::::::::::::L   OO:::::::::OO        CCC::::::::::::CK:::::::K    K:::::K
     000000000     xxxxxxx      xxxxxxxLLLLLLLLLLLLLLLLLLLLLLLL     OOOOOOOOO             CCCCCCCCCCCCCKKKKKKKKK    KKKKKKK
                                                                                                                                                                                                                                                    

"""+ Style.RESET_ALL)
    print(Fore.GREEN + """
        
                ▌▌  ▄▖▄▖▄▖▄▖▖▖▄▖▄▖▄▖▄   ▄▖▖▖▄▖▄▖▄▖▖  ▖   ▌ ▌  ▖ ▄▖  ▖▖  ▄▖▄▖▄▖▄▖▖▖▄▖  ▐▘▄▖▄▖▄▖▄▖▄▖▜   ▌▌
                ▌▌  ▌ ▌▌▙▘▙▘▌▌▙▌▐ ▙▖▌▌  ▚ ▌▌▚ ▐ ▙▖▛▖▞▌  ▐ ▐   ▌ ▛▌▛▘▙▘  ▌▌▌ ▐ ▐ ▌▌▙▖  ▐ ▙▖▙▘▙▘▌▌▙▘▐   ▌▌
                ▖▖  ▙▖▙▌▌▌▌▌▙▌▌ ▐ ▙▖▙▘▄▖▄▌▐ ▄▌▐ ▙▖▌▝ ▌  ▞ ▞   ▙▖█▌▙▖▌▌▄▖▛▌▙▖▐ ▟▖▚▘▙▖  ▐ ▙▖▌▌▌▌▙▌▌▌▐   ▖▖
                                                        ▘ ▘                           ▝▘          ▀     

""")
def fake_boot():
    type_out(Fore.GREEN + "Secure boot completed.")
    type_out(Fore.GREEN +"Running integrity checks...\n")
    time.sleep(0.8)
    type_out(Fore.GREEN + f"Subsystems: POWER - OK | DOORS - LOCKED | AUTH - {attempts} ATTEMPTS")
    type_out(Fore.GREEN +"Use `help` to view command list.\n")

def list_commands():
    print(Fore.GREEN + Style.BRIGHT + "\nAVAILABLE COMMANDS:")
    print("LIST            - View visible system files")
    print("VIEW <file>     - Display contents of a file")
    print("MEMDUMP         - Display memory sectors (warning: restricted)")
    print("AUTH            - Attempt authentication")
    print("HELP            - Show this help menu")
    print("RESTART         - Reboot interface")
    print("EXIT            - Close session\n")

    if unlocked:
        print("LIST -A         - View all system files (requires level 2 access)")
        print("DECRYPT         - Decrypt protected files")
        print("ANALYZE         - Run memory pattern analysis")
        print("UNLOCK <file>   - Attempt to unlock a restricted file (requires level 2 access)")
        
        print("ADMIN           - Log As admin")
def list_files(hidden=False):
    print(Fore.GREEN + "\n> DIRECTORY: /mnt/sec/")
    print(" - system.log")
    print(" - auth_records.txt")
    print(" - vault.log" + Style.RESET_ALL)
    if hidden:
        print(Fore.GREEN + " - .memdump_cache")
        print(Fore.GREEN + " - .emergency_override"+ Style.RESET_ALL)

def generate_memory_dump():
    global password_address
    dump = []
    password_line = random.randint(0, 15)  # Choose random line (0-15)
    password_pos = random.randint(0, 1)    # Choose position in line (0 or 1)
    ok = 0
    
    for line_num in range(16):
        addr = "0x" + ''.join(random.choices("ABCDEF0123456789", k=4))
        line = addr + " "
        
        if line_num == password_line:
            password_address = addr  # Store the correct addresss            
        for chunk_num in range(2):
            chunk = ""
            for _ in range(8):
                if line_num == password_line and chunk_num == password_pos and ok == 0:
                    # Place the correct password exactly once
                    chunk += CORRECT_PASSWORD.ljust(8)
                    dump.append((CORRECT_PASSWORD, addr))
                    ok = 1
                else:
                    if random.random() < 0.2:
                        # Place incorrect passwords
                        word = random.choice([w for w in PASSWORDS if w != CORRECT_PASSWORD])
                        chunk += word.ljust(8)
                        dump.append((word, addr))
                    else:
                        # Place junk characters
                        chunk += ''.join(random.choices(JUNK_CHARS, k=8))
            line += chunk + " "
        print(line)
    return dump

def view_file(file):
    file = file.lower()
    if file == "system.log":
        type_out(Fore.GREEN + "\n> Opening system.log..." )
        time.sleep(0.8)
        type_out(Fore.GREEN + """

☠ ▓▓▓▓▓ SYSTEM.LOG — CORRUPTED ENTRY ▓▓▓▓▓ ☠
▓  >> OPENING SYSTEM.LOG...
▓  >> LAST ATTEMPT: FAILED (CODE INVALID)
▓  >> EMERGENCY CODES ENABLED: TRUE
▓
▓  >> WARNING: UNAUTHORIZED ACCESS DETECTED
▓  >> USER: [REDACTED] 
▓  >> LOCATION: [REDACTED] 
▓  >> TIME: [REDACTED] 
▓
▓  >> SECURITY OVERRIDE INITIATED
▓  >> COUNTDOWN TO LOCKDOWN: ████░░░░░░ 40%
▓
▓  >> LAST MESSAGE: "THEY KNOW YOU'RE HERE"
▓  >> TRANSMISSION ENDS IN 5...4...3...
▓
☠ ▓▓▓▓▓ TERMINATE CONNECTION IMMEDIATELY ▓▓▓▓▓ ☠

""" + Style.RESET_ALL)
    elif file == "auth_records.txt":
        type_out(Fore.GREEN + "\n> Opening auth_records.txt...")
        type_out(Fore.GREEN + """

☠ ▓▓▓▓▓ AUTHENTICATION LOG — LOCKOUT IMMINENT ▓▓▓▓▓ ☠
▓  >> SCANNING HISTORY...  
▓  >> WARNING: 11 FAILED ATTEMPTS DETECTED   
▓  
▓  >> FAILED ATTEMPTS:  
▓     1. 1987-10-25 14:32:11 - FAILED  
▓     2. 1996-11-15 14:33:45 - FAILED  
▓     3. 1996-11-15 14:33:45 - FAILED  
▓     4. 1998-11-15 14:33:45 - FAILED [LOCKOUT TRIGGER]  
▓     5. 1998-11-15 14:33:45 - FAILED  
▓     6. 2000-11-15 14:33:45 - FAILED  
▓     7. 2001-11-15 14:33:45 - FAILED  
▓     8. 2001-11-15 14:33:45 - FAILED  
▓     9. 2024-04-23 00:00:01 - FAILED  
▓    10. 2025-04-23 00:00:02 - FAILED  
▓    11. 1987-10-25 14:32:12 - FAILED [TEMPORAL ANOMALY]  
▓  
▓  >> SECURITY ALERT:  
▓     ░░ 4 FAILED ATTEMPTS DETECTED ░░  
▓     ░░ SYSTEM LOCKOUT IN 00:30 ░░  
▓  
▓  >> FINAL WARNING:  
▓     "TRY TO FIND THE SECRET MESSAGE AND SAVE US"  
▓  
☠ ▓▓▓▓▓ TERMINATE SESSION TO AVOID CONTAINMENT ▓▓▓▓▓ ☠  

"""+ Style.RESET_ALL)

    elif file == "vault.log":
        if unlocked:
            type_out(Fore.GREEN + "\n> Opening vault.log..." )
            type_out(Fore.GREEN + "\nKEY: \n")
            type_out(Fore.GREEN +  """
            SSBrbm93IHlvdSdyZSBsb29raW5nIGZvciBhIGtleS4gSSBjb3VsZCBqdXN0IGdpdmUgaXQgdG8geW91IGRlY3J5cHRlZOKApiBidXQgd2hlcmXigJlzIHRoZSBmdW4gaW4gdGhhdD8gSW5zdGVhZCwgaGVyZeKAmXMgdGhlIGtleeKAlGVuY3J5cHRlZCwgb2YgY291cnNlOiAKU29ycnnigKYgb3IgbWF5YmUgbm90PyBQZXJoYXBzIHRvbW9ycm93IEnigJlsbCBiZSBnZW5lcm91c+KApiBvciBwZXJoYXBzIG5vdC4gKExldOKAmXMgYmUgaG9uZXN04oCUcHJvYmFibHkgbm90LikKUmVtZW1iZXIsIHRoZSBhZG1pbiBwYXNzd29yZCBpc27igJl0IG1lYW50IHRvIGJlIGhhbmRlZCBvdXQgZWFzaWx5LiBXZSBjYW7igJl0IHJpc2sgaXQgZmFsbGluZyBpbnRvIHRoZSB3cm9uZyBoYW5kcy4KClF2cSBWIHdoZmcgam5mZ3IgbGJoZSBndnpyPyBCYmNm4oCmIEZiZWVsPyAoQnhubCwgem5sb3IgViBxYiBzcnJ5IG4geXZnZ3lyIG9ucS4pClYgY2VienZmciBndXZmIHZmIGd1ciB5bmZnIGd2enIgViBnZXZweCBsYmjigKYgYmUgbmcgeXJuZmcsIGd1ciB5bmZnIGd2enIgZ2JxbmwuClVyZXLigJlmIGd1ciByYXBlbGNncnEgeHJs4oCUc2JlIGVybnkgZ3V2ZiBndnpyOgoKODNicTQ4M2JxNCtISG9MUitZLztRc2cmdkU7aHddUVdmST5RLi1oN1c+QlUsUXNxK1FPQkQhKk95eFdOUXNieSwrUlpLUFIkMCIvLzBXUVJTPFQ3LlUvbkA9OGBUOHRRJzNkQFUidS8vK1JJQVJASSRbJFFyZi0wTlhMTGdSby13VD1gOFMqUVZ6T3YrUERQLk5ILFExUXNEZ09PQ1FBPStReEM0QEklKTVQMz1HPitReEM0QEklKTVTUSw1LlBZZHA2T3lvUT1PQmU8Lk95YTAmK1IodzdTUSxPMCtQcyhhUHYhWyNPNEpcJiQ/Ly1kM11YLHQ+OVRbbjZHRTFyN1Uvdl5UR1xnKDczU0pbOmBnISo0P3kpJT5jK05cdnFxU28rPztcRjZHRSJxMlYuVFY0TTVXXjU9Vj1jOHQjaFkxcW55JDc2M1toPjlVOXgxLVZwelFPQSMjN0VcU1syVC4wZTU8Yz5JMmBSSk02YkIlR0NKUTd6Vz0vclc0JTtJLCtARkJcKz5naFA4ekNCK1VhYTtaMk9MQlgrPnA+RDRNKz9BNkk/P3RJT04sbj45Vy81MipuUHBXPS91WDQ/eSkldnFxelgxKk5aNjgwUCldNkcvdClWRSQxcnZxcTduMS0udy4rP0ElXDczU3ZbMk9MMVg2Ry8teDZHRTFyNztgVD4/S0U1Vz9LRThYK1BOWm4/S0U1Vz96JnNuP2ZxO1k/Zm8kYD9mej5YP2ZxOm4/S1YyVz9mek5ZK1BOV2A/S1YvVj9EYF1gP0tFOFg/S0MhYD9mej5ZP2Z6QG8/S0U4WT9LRTVYK1BOV2A/S1YvVj9EYF1gP2Z6Plk/Zngqbj9mej5ZP0tWMWA/S0U4WD9mek5ZK1BOV2A/S0U4WT9EYF1fP2ZxOFc/S1NjXz9mcThYP0tWLl8/S0U4WD9LRTVYK1BOWm4/ZnE4WD9EYF1gP2ZxOFg/S0MhYD9LRTVXP2Z6QG8/S0U4WT9LVjJYK1BOV2A/S1YvVj9EYF1gP2Z6Tlk/S0MhYD9mej5ZP2Z6QG8/S0U4WT9LRTVYK1BOWm4/ZnE4WD9EYF1fP2ZxOFc/S1NjXz9mej5ZP0tFN24/S0U4WD9LRTVYK1BOWm4/Zno+WD96JnNgP2ZxO1k/Zm8kYD9LVi9XP0tFNGA/S0U1Vz9LRTVXK1BOWm4/S0U4WT96JnNuP2ZxO1k/Zm8kYD9LRTVXP2Z6QG8/S0U4WT9LRTVXK1BOV2A/S1YvVj9EYF1gP2ZxOFg/S0MhYD9mek5aP0tWLl8/S0U4WT9LVi9WK1BOWm4/S1YyVz96JnNuP2ZxOFc/Zngqbj9mek5ZP2ZxN2A/S1YyVz9LVi9WK1BOWm4/S1YvVj96JnNuP2Z6Plg/S1NjXz9mek5ZP0tWLl8/S0U4WD9mej5YK1BOWm4/S1YvVj96JnNuP2Z6Plk/S0MhYD9mek5ZP0tFN24/S0U4WD9LRTVYK1BOV2A/S1YvVj9EYF1fP2ZxO1k/S0MhYD9LRTVXP0tWLl8/S0U4WD9LVjJXK1BOWm4/ZnE4WD9EYF1gP2ZxOFg/S0MhYD9mej5YP0tWMWA/S0U4WD9mcTtZK1BOWm4/S0U1Vz96JnNuP2ZxO1k/Zm8kYD9mej5YP2Z6QG8/S1YyVz9LVi9WK1BOWm4/S1YyVz96JnNuP2ZxO1k/S1NjXz9mej5YP2ZxOm4/S0U4WD9mej5ZK1BOWm4/S1YyVz96JnNuP2ZxO1k/Zm8kYD9mek5ZP2ZxN2A/S0U4WD9LVi9XK1BOWm4/ZnE4WD9EYF1gP2Z6Tlk/S0MhYD9LRTVXP0tWLl8/S0U4WD9LRTVYK1BOWm4/S0U4WT9EYF1gP2ZxOFc/Zngqbj9mek5ZP0tFNGA/S0U4WT9mcThYK1BOWm4/ZnE4Vz9EYF1gP2Z6Plk/S1NjXz9mej5ZP0tWMWA/S0U4WD9mek5aK1BOWm4/S0U4WT9EYF1fP2ZxOFc/S1NjXz9mej5ZP0tWMWA/S0U4WT9LVjJYK1BOWm4/S0U4WT9EYF1fP2ZxOFg/Zngqbj9mek5ZP2ZxN2A/S1YyVz9LVi9WK1BOWm4/S1YyVz96JnNuP2Z6Tlk/S1NjXz9mej5YP0tWMWA/S0U4WD9LVjJYK1BOWm4/ZnE7WD9EYF1gP2ZxO1k/S1NjXz9mek5aP0tWMWA/S1YyVz9LVi9WK1BOWmA/S0U4WT9EYF1gP2ZxO1k/Zngqbj9mej5YP0tFNGA/S0U4WD9LRTVYK1BOWm4/S0U4WD9EYF1fP2ZxOFc/S1NjXz9mcTtYP0tWLl8/S0U4WT9LVjJXK1BOWm4/S0U1Vz96JnNuP2Z6Tlk/Zm8kYD9mej5YP2ZxOm4/S1YyVz9LVi9WK1BOWm4/S0U4WD96JnNuP2ZxOFc/S0MhYD9mek5ZP2ZxN2A/S0U4WD9LRTVYK1BOWm4/ZnE4WD9EYF1gP2ZxO1g/S0MhYD9mej5YP0tWMWA/S0U4WD9mej5YK1BOV2A/S0U4WT9EYF1fP0tWMlc/Zm8kYD9LVi9XP0tFNGA/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNuP0tFOFg/Zngqbj9LRThZP2Z6PW4/S1YyVz9mcTtZK1BOV2A/ZnpOWj9EYF1fP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/ZnpOWj9EYF1fP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/ZnpOWj9EYF1fP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyWD9mej5YK1BOV2A/ZnpOWT9EYF1fP2Z6Tlo/S1NjXz9LRThZP2ZxN2A/S1YyVz9mej5ZK1BOWmA/ZnpOWT96JnNgP2Z6Tlo/Zm8kYD9LRThZP2Z6PW4/S1YyWD9mek5ZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP2Z6PW4/S1YyWD9mek5ZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U4WT9EYF1fP2ZxO1g/Zngqbj9LRTVYP2Z6PW4/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1k/Zm8kYD9LRThZP2ZxN2A/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2Z6PW4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mek5ZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mek5ZK1BOV2A/ZnpOWj9EYF1fP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WT9EYF1fP2Z6Tlo/S1NjXz9LRThZP2ZxN2A/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U4WT9EYF1fP2Z6Tlo/Zm8kYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mek5ZK1BOV2A/ZnpOWT9EYF1fP2ZxO1k/Zm8kYD9LRThZP2Z6PW4/S1YyWD9mek5ZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1k/Zm8kYD9LRThZP2ZxN2A/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2Z6PW4/S1YyWD9mej5YK1BOV2A/S0U1WD96JnNgP2ZxO1k/Zm8kYD9LRThZP2Z6PW4/S1YyWD9mek5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/Zm8kYD9LRTVYP2Z6PW4/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U1WD96JnNgP2ZxO1g/Zngqbj9LRTVYP0tFN24/S1YyVz9mcTtZK1BOV2A/S0U4WT9EYF1fP2Z6Tlo/S1NjXz9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mej5ZK1BOV2A/S0U4WD96JnNgP2ZxO1k/S0MhYD9LRTVYP2ZxOm4/S1YyVz9mek5Z

           """ + Style.RESET_ALL)
        else:
            type_out(Fore.RED + "\n> ACCESS DENIED. FILE IS LOCKED 🔒\n" + Style.RESET_ALL)
            type_out(Fore.RED + "Requires authentication level 2" + Style.RESET_ALL)
    elif file == ".memdump_cache":
        if unlocked_admin:
            type_out(Fore.GREEN + """01010100 01101000 01100101 00100000 01100001 01100010 01110011 01100101 01101110 01100011 01100101 00100000 01101111 01100110 00100000 01101100 01101001 01100111 01101000 01110100 00100000 01100100 01101111 01100101 01110011 01101110 00100111 01110100 00100000 01100101 01110001 01110101 01100001 01101100 00100000 01100001 01100010 01110011 01100101 01101110 01100011 01100101 00100000 01101111 01100110 00100000 01101100 01101001 01100110 01100101 00100000 00101101 00100000 01110001 01110101 01101001 01110100 01100101 00100000 01110100 01101000 01100101 00100000 01101111 01110000 01110000 01101111 01110011 01101001 01110100 01100101 00101110 00100000 01010110 01101001 01110011 01101001 01100010 01101001 01101100 01101001 01110100 01111001 00100000 01101001 01110011 00100000 01100001 00100000 01110000 01110010 01101001 01110110 01101001 01101100 01100101 01100111 01100101 00100000 01110100 01101000 01100101 00100000 01110101 01101110 01110011 01100101 01100101 01101110 00100000 01100100 01101111 01101110 00100111 01110100 00100000 01110010 01100101 01110001 01110101 01101001 01110010 01100101 00101110 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00001010 00111000 00110101 00100000 00111000 00110110 00100000 00111000 00110100 00100000 00110001 00110010 00110011 00100000 00111000 00110100 00100000 00110001 00110000 00110100 00100000 00110101 00110001 00100000 00111001 00110101 00100000 00110001 00110000 00111001 00100000 00110101 00110001 00100000 00111001 00111001 00100000 00110001 00110000 00110100 00100000 00110101 00110010 00100000 00110001 00110001 00110000 00100000 00110100 00111001 00100000 00110001 00110001 00110101 00100000 00110111 00110111 00100000 00111001 00110101 00100000 00111000 00110101 00100000 00110111 00111000 00100000 00110001 00110001 00110101 00100000 00110101 00110001 00100000 00111001 00110111 00100000 00110100 00111001 00100000 00110101 00110011 00100000 00111001 00110101 00100000 00110101 00110010 00100000 00110001 00110001 00110000 00100000 00110001 00110000 00110000 00100000 00111001 00110101 00100000 00110001 00110001 00110110 00100000 00110111 00110010 00100000 00110101 00110001 00100000 00111001 00110101 00100000 00110110 00111000 00100000 00111001 00110111 00100000 00111000 00110010 00100000 00110111 00110101 00100000 00111001 00110101 00100000 00110001 00110001 00110111 00100000 00110111 00111000 00100000 00110110 00110110 00100000 00110001 00110000 00111000 00100000 00110100 00111001 00100000 00110001 00110001 00110000 00100000 00110001 00110000 00110111 00100000 00110101 00110011 00100000 00110001 00110010 00110101
            """)
        else:
            type_out(Fore.RED + "\n> INSUFFICIENT PRIVILEGES\n" + Style.RESET_ALL)
            type_out(Fore.RED + "Requires authentication level 3(admin)")
    elif file == ".emergency_override":
        type_out(Fore.RED + "\n> FILE IS ENCRYPTED 🔒" + Style.RESET_ALL)

    else:
        type_out(Fore.RED + f"\n> FILE '{file}' NOT FOUND." + Style.RESET_ALL)

def handle_auth():
    global attempts, unlocked, password_timeout
    
    current_time = time.time()
    if current_time < password_timeout:
        remaining = int(password_timeout - current_time)
        type_out(Fore.RED + f"\n> SECURITY LOCKOUT: Wait {remaining} seconds" + Style.RESET_ALL)
        return
    
    if attempts <= 0:
        type_out(Fore.RED + "> TERMINAL LOCKED. PLEASE CONTACT ADMIN. " + Style.RESET_ALL)
        return
    
    type_out("> ENTER MEMORY DUMP PASSWORD:\n")
    guess = input(Fore.RED + "PASSWORD> ").strip().upper()
    
    if guess == CORRECT_PASSWORD:
        type_out(Fore.GREEN + "\n> PASSWORD ACCEPTED" + Style.RESET_ALL)
        type_out(Fore.GREEN + "\n> GRANTING LEVEL 2 ACCESS...")
        unlocked = True
        time.sleep(1)
        type_out(Fore.GREEN + "\nNEW COMMANDS AVAILABLE:\n")
        print(Fore.GREEN +"LIST -A         - View all system files (requires level 2 access)")
        print(Fore.GREEN +"DECRYPT         - Decrypt protected files")
        print(Fore.GREEN +"ANALYZE         - Run memory pattern analysis")
        print(Fore.GREEN +"UNLOCK <file>   - Attempt to unlock a restricted file (requires level 2 access) " + Style.RESET_ALL)

    else:  # Failed attempt
        attempts -= 1
        delay = (5 - attempts) * 2  # Exponential cooldown
        password_timeout = time.time() + delay
    
        type_out(Fore.RED + f"> ACCESS DENIED (Cooldown: {delay}s)\n")
        type_out(Fore.RED + f"> WARNING: {attempts} ATTEMPT(S) REMAINING" + Style.RESET_ALL)
    
    if attempts == 0:
        type_out(Fore.RED + "\n> FATAL LOCKOUT INITIATED\n")
        print(Fore.RED + "> TERMINAL DISABLED. CONTACT SECURITY ADMIN"+ Style.RESET_ALL)
def unlock_file(file):
    global unlocked
    if not unlocked:
        type_out(Fore.RED + "\n> AUTHENTICATION REQUIRED"+ Style.RESET_ALL)
        return
    
    file = file.lower()
    if file == "vault.log":
        type_out(Fore.RED + "\n> Enter memory address where memory corruption was detected:\n")
        addr = input(Fore.RED +"ADDR> ")
        if addr == password_address:
            type_out(Fore.GREEN + "\n> ADDRESS VERIFIED"+ Style.RESET_ALL)
            type_out(Fore.GREEN + "\n> UNLOCKING VAULT.LOG..."+ Style.RESET_ALL)
            time.sleep(2)
            view_file("vault.log")
        else:
            type_out(Fore.RED + "> INVALID ADDRESS"+ Style.RESET_ALL)
    else:
        type_out(Fore.RED + f"> Cannot unlock '{file}'"+ Style.RESET_ALL)

def run_diagnostic():
    type_out(Fore.GREEN + "\n> Running diagnostic...\n")
    time.sleep(1)
    type_out(Fore.GREEN + "Checking secure files...\n")
    type_out(Fore.GREEN + "vault.log - STATUS: LOCK 🔒\n")
    type_out(Fore.GREEN + f"Memory corruption detected in sector {password_address}"+ Style.RESET_ALL)

def decrypt_file(file):
    if file == ".emergency_override":
        type_out("\n> Decryption requires a key:")
        addr = input("KEY> ")
        if addr == "ThisI5Th3K3yH4ppy?":
            type_out(Fore.GREEN + "> ADDRESS VERIFIED")
            type_out("> DECRYPTING .emergency_override...")
            time.sleep(2)
            type_out("")
            type_out("> Opening .emergency_override")
            time.sleep(1)
            type_out("")
            type_out(Fore.GREEN + """
☠ ▓▓▓▓▓ EMERGENCY ADMINISTRATOR LOCKOUT [CRITICAL] ▓▓▓▓▓ ☠

▓  >> SYSTEM CORRUPTION: PHASE 3
▓  >> DECRYPTION ATTEMPT #13 FAILED
▓
▓  >> n = 23952937352643527451379227516428377705004894508566304313177880191662177061878993798938496818120987817049538365206671401938265663712351239785237507341311858383628932183083145614696585411921662992078376103990806989257289472590902167457302888198293135333083734504191910953238278860923153746261500759411620299864395158783509535039259714359526738924736952759753503357614939203434092075676169179112452620687731670534906069845965633455748606649062394293289967059348143206600765820021392608270528856238306849191113241355842396325210132358046616312901337987464473799040762271876389031455051640937681745409057246190498795697239
▓  >> c = 6627726821160884181237560680843788453116774093381811995505362415530384527079368412488855896822255982052975348880709871994141777296402739766183671442566359154291342660955457342507654275141819203352743073455321252374747629860499466775559531823727500029495614975369019911510161139550685611132120575254719189241984655735043782562955614589479077937885237800618075475433866679137724062290068587755815948070793246910421403217134751717965333615025647822241139809878192573894877545323602760329951111851061103135229304631437887862517607640372460362364263423277011061708749598079064485480678103553929752846379524358142008669396
▓
▓  !! WARNING: ADMIN KEY REQUIRED
▓     ░░ YOU ARE BEING WATCHED ░░
▓
▓  >> THE KEY WAS INSIDE YOU ALL ALONG
▓  >> (METAPHORICALLY. OR NOT.)
▓
▓  >> COUNTDOWN: ███████░░░ 70%
▓

☠ ▓▓▓▓▓ THIS MESSAGE WILL SELF-DESTRUCT IN 30 ▓▓▓▓▓ ☠
""")
        else:
            type_out(Fore.RED + "> INVALID ADDRESS"+ Style.RESET_ALL)
    else:
        type_out(Fore.RED + f"> Cannot unlock '{file}'"+ Style.RESET_ALL)

password_timeout = 0

def handle_admin():

    global attempts_admin, password_timeout, unlocked_admin
    
    current_time = time.time()
    if current_time < password_timeout:
        remaining = int(password_timeout - current_time)
        type_out(Fore.RED + f"\n> SECURITY LOCKOUT: Wait {remaining} seconds"+ Style.RESET_ALL)
        return
    
    if attempts_admin <= 0:
        type_out(Fore.RED + "> TERMINAL LOCKED.\n")
        return
    
    type_out("\n> ENTER PASSWORD:\n")
    guess = input(Fore.RED + "\nPASSWORD> ")
    
    if guess == 'Adm1NP4a55wordNoTS0Secure':  
        type_out(Fore.GREEN + "\n> ADMIN PRIVILEGES DETECTED")
        type_out(Fore.GREEN + "\n> OVERRIDING SECURITY PROTOCOLS...")
        unlocked_admin = True
        time.sleep(1.5)
        type_out(Fore.GREEN + """

☠ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ☠

> YOU SHOULDN'T BE HERE.  
> TURN BACK NOW.

☠ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ☠

""")
        time.sleep(2)
        type_out(Fore.GREEN + """

▓  >> LAST WARNING: REMAINING  
▓  >> SYSTEM STATUS: [CORRUPTION DETECTED]  
▓  >> LOCKS ENGAGED IN: [00:30]  

""")

        time.sleep(1)
        type_out(Fore.GREEN + """ 

■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
----------- [UNAUTHORIZED ACCESS DETECTED] ---------
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

▓  >> MESSAGE: "THEY SEE YOU"  
▓  >> NOTICE: THIS SESSION IS BEING RECORDED  
▓  >> FINAL ALERT: IT'S ALREADY TOO LATE  
▓  >> WAIT FOR THE LOG IN 

""")

        time.sleep(3)
        type_out(Fore.GREEN + """
☠ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ☠

▓> WELCOME BACK, ADMIN. SYSTEMS AT YOUR DISPOSAL. ♡ 
▓
▓  >> LAST ACCESS: [REDACTED]  
▓  >> LOCATION: [REDACTED]  
▓  >> BIOMETRICS: [MATCH 87%]  

■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
----------- [FULL SYSTEM ACCESS GRANTED] -----------
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

▓  >> WARNING: 23 ACTIVE SURVEILLANCE FEEDS  
▓  >> NOTICE: YOU ARE THE ONLY ADMIN IN DATABASE  
▓  >> SYSTEM: "THEY KNOW YOU'RE HERE"  

☠ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ☠

"""+ Style.RESET_ALL) 

    else:  # Failed attempt
        attempts_admin -= 1
        delay = (5 - attempts) * 2  # Exponential cooldown
        password_timeout = time.time() + delay
    
        type_out(Fore.RED + f"> ACCESS DENIED (Cooldown: {delay}s)" + Style.RESET_ALL)
        type_out(Fore.RED + f"> WARNING: {attempts_admin} ATTEMPT(S) REMAINING"+ Style.RESET_ALL)
    
def main():
    clear()
    terminal_header()
    fake_boot()

    while True:
        try:
            cmd = input(Fore.GREEN + Style.BRIGHT + "\nVAULT> ").strip().lower()

            if cmd == "help":
                list_commands()
            elif cmd == "list":
                list_files()
            elif cmd == "list -a" and unlocked:
                    list_files(hidden=True)
            elif cmd.startswith("view "):
                _, file = cmd.split(" ", 1)
                view_file(file)
            elif cmd == "memdump":
                generate_memory_dump()
            elif cmd == "auth":
                handle_auth()
            elif cmd.startswith("unlock ") and unlocked:
                _, file = cmd.split(" ", 1)
                unlock_file(file)
            elif cmd == "analyze" and unlocked:
                run_diagnostic()
            elif cmd.startswith("decrypt ") and unlocked:
                _, file = cmd.split(" ", 1)
                decrypt_file(file)
            elif cmd == "restart":
                type_out(Fore.GREEN + "Restarting terminal..." )
                time.sleep(1)
                clear()
                terminal_header()
                fake_boot()
            elif cmd == "admin" and unlocked:
                handle_admin()
            elif cmd in ["exit", "quit"]:
                type_out(Fore.GREEN + "Logging out..." + Style.RESET_ALL)
                break
            else:
                type_out(Fore.RED + "Unrecognized command. Type HELP!" + Style.RESET_ALL)
                
        except KeyboardInterrupt:
            type_out(Fore.RED + "\n> SECURITY ALERT: Unauthorized interruption" + Style.RESET_ALL)
            break
        except:
            type_out(Fore.RED + "> SYSTEM ERROR" + Style.RESET_ALL)

if __name__ == "__main__":
    main()