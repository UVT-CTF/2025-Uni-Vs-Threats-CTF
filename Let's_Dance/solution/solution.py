from Crypto.Util.number import bytes_to_long
from Crypto.Util.Padding import pad
from pwn import xor
import random

# given
ct1 =  b'\xed\x82\x01\x94\xdf\t\xef\xefN\xf8\xec$7\x96\xa8\x9e\x0eJ%j\x07\x00A\xfb\x9e\x9f\x9b~s\x96H\x1cS\xdc\x92\xdd\xca\x9e\x9d\xf1'
ct2 =  b'\xed\x82\x01\x94\xdf\t\xef\xef{\xdc\xe8IN\xd0\x92\xf7\x06M6t@0M\x98'

def random_shuffle(p, n):
    l = list(p)
    random.seed(bytes_to_long(n))
    random.shuffle(l)
    p = bytes(l)
    return p

def unshuffle(p, n):
    l = list(p)
    lcpy = l.copy()
    
    # shuffle an index list using the same seed
    indices = [i for i in range(len(l))]
    random.seed(bytes_to_long(n))
    random.shuffle(indices)
    
    # sort the string based on shuffled indices
    for i in range(len(l)):
        lcpy[indices[i]] = l[i]
    p = bytes(lcpy)
    return p

def decrypt_with_move(move):
    # trim nonce
    enc_text = ct1[8:] 
    enc_flag = ct2[8:]
    # get nonce for shuffle seed
    nonce = ct1[:8] 

    # rebuild the text before encryption (padded and shuffled)
    text = pad(move, 16)
    text = random_shuffle(text, nonce)

    # recover keystream, decrypt and un-shuffle result
    keystream = xor(text, enc_text)
    decrypted = xor(keystream[:len(enc_flag)], enc_flag)
    result = unshuffle(decrypted, nonce)
    
    return result

if __name__ == "__main__":
    with open("moves.txt", "r") as f:
        moves_list = eval(f.read())

    for move in moves_list:
        try:
            flag = decrypt_with_move(bytes(move, encoding='utf-8'))
            flag = flag.decode("utf-8")
            if flag[:3] == "UVT":
                print(flag)
        except:
            continue