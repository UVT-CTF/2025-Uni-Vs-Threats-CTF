from Crypto.Util.number import bytes_to_long
from Crypto.Util.Padding import pad
from Crypto.Cipher import Salsa20
import secrets
import random

k = secrets.token_bytes(32)
n = secrets.token_bytes(8)

def get_salsa_move():
    with open("moves.txt", "r") as f:
        moves_list = eval(f.read())
    move = random.choice(moves_list)
    return move

def random_shuffle(x):
    l = list(x)
    random.seed(bytes_to_long(n))
    random.shuffle(l)
    x = bytes(l)
    return x

def encrypt(x):
    p = pad(x, 16)
    s = random_shuffle(p)
    cipher = Salsa20.new(k, n)
    return cipher.nonce + cipher.encrypt(s)

if __name__ == "__main__":
    move = bytes(get_salsa_move(), encoding='utf-8')
    flag = b'UVT{ju5t_f33l_th3_r1thm}'

    print("ct1 = ", encrypt(move))
    print("ct2 = ", encrypt(flag))
