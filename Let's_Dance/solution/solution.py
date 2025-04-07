from Crypto.Util.number import bytes_to_long
from Crypto.Util.Padding import pad
from pwn import xor
import random

# given
ct1 =  b'\x90\xbb\x06\xccj>\xdfj\x9d\xe0\x7f\xc7\xad\x8fNyfI\x96\x9e\x1f\x85\xa9\x07\x8f\xdd\xf1f@\xea\x8a-\x1c\xb55\xb2\xd6\xc0+\x98'
ct2 =  b'\x90\xbb\x06\xccj>\xdfj\x9b\xac#C\xf0\x89-\x7fc\\\x90(\x14\x83\xa6\x02\xb5\xa7\xce`U\xf2\x8cRo\xe43\x8b\xe6\xa6W\x8a'

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
    decrypted = xor(keystream, enc_flag)
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