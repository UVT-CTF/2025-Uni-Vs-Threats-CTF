from pwn import *
from Crypto.Util.number import long_to_bytes

class RandGuesser:

    def __init__(self):
        self.counter = 0
        self.mt = []
        self.state = False

    def submit(self, num):
        if self.state:
            raise ValueError("Already got enough bits")

        bits = self._to_bitarray(num)

        assert (all([x == 0 or x == 1 for x in bits]))
        self.counter += 1
        self.mt.append(self._harden_inverse(bits))
        if self.counter == 25:
            self._regen()
            self.state = True

    def _predict_32(self):
        if not self.state:
            raise ValueError("Didn't recieve enough bits to predict")

        if self.counter >= 25:
            self._regen()
        self.counter += 1

        return self._harden(self.mt[self.counter - 1])

    def predict_getrandbits(self, k):
        if not self.state:
            raise ValueError("Didn't recieve enough bits to predict")

        if k == 0:
            return 0
        words = (k - 1) // 32 + 1
        res = []
        for i in range(words):
            r = self._predict_32()
            if k < 32:
                r = [0] * (32 - k) + r[:k]
            res = r + res
            k -= 32
        return self._to_int(res)

    def predict_randbelow(self, n):
        k = n.bit_length()
        r = self.predict_getrandbits(k)
        while r >= n:
            r = self.predict_getrandbits(k)
        return r

    def predict_randrange(self, start, stop=None, step=1, _int=int):
        # Adopted messy code from random.py module
        # In fact only changed _randbelow() method calls to predict_randbelow()
        istart = _int(start)
        if istart != start:
            raise ValueError("non-integer arg 1 for randrange()")
        if stop is None:
            if istart > 0:
                return self.predict_randbelow(istart)
            raise ValueError("empty range for randrange()")

        # stop argument supplied.
        istop = _int(stop)
        if istop != stop:
            raise ValueError("non-integer stop for randrange()")
        width = istop - istart
        if step == 1 and width > 0:
            return istart + self.predict_randbelow(width)
        if step == 1:
            raise ValueError("empty range for randrange() (%d,%d, %d)" % (istart, istop, width))

        # Non-unit step argument supplied.
        istep = _int(step)
        if istep != step:
            raise ValueError("non-integer step for randrange()")
        if istep > 0:
            n = (width + istep - 1) // istep
        elif istep < 0:
            n = (width + istep + 1) // istep
        else:
            raise ValueError("zero step for randrange()")

        if n <= 0:
            raise ValueError("empty range for randrange()")

        return istart + istep * self.predict_randbelow(n)

    def predict_randint(self, a, b):
        return self.predict_randrange(a, b + 1)

    def predict_choice(self, seq):
        try:
            i = self.predict_randbelow(len(seq))
        except ValueError:
            raise IndexError('Cannot choose from an empty sequence')
        return seq[i]

    def predict_random(self):
        a = self._to_int(self._predict_32()) >> 5
        b = self._to_int(self._predict_32()) >> 6
        return ((a*67108864.0)+b)/9007199254740992.0

    def _to_bitarray(self, num):
        k = [int(x) for x in bin(num)[2:]]
        return [0] * (32 - len(k)) + k

    def _to_int(self, bits):
        return int("".join(str(i) for i in bits), 2)

    def _or_nums(self, a, b):
        if len(a) < 32:
            a = [0] * (32 - len(a)) + a
        if len(b) < 32:
            b = [0] * (32 - len(b)) + b

        return [x[0] | x[1] for x in zip(a, b)]

    def _xor_nums(self, a, b):
        if len(a) < 32:
            a = [0] * (32 - len(a)) + a
        if len(b) < 32:
            b = [0] * (32 - len(b)) + b

        return [x[0] ^ x[1] for x in zip(a, b)]

    def _and_nums(self, a, b):
        if len(a) < 32:
            a = [0] * (32 - len(a)) + a
        if len(b) < 32:
            b = [0] * (32 - len(b)) + b

        return [x[0] & x[1] for x in zip(a, b)]

    def _decode_harden_midop(self, enc, and_arr, shift):

        NEW = 0
        XOR = 1
        OK = 2
        work = []
        for i in range(32):
            work.append((NEW, enc[i]))
        changed = True
        while changed:
            changed = False
            for i in range(32):
                status = work[i][0]
                data = work[i][1]
                if i >= 32 - shift and status == NEW:
                    work[i] = (OK, data)
                    changed = True
                elif i < 32 - shift and status == NEW:
                    if and_arr[i] == 0:
                        work[i] = (OK, data)
                        changed = True
                    else:
                        work[i] = (XOR, data)
                        changed = True
                elif status == XOR:
                    i_other = i + shift
                    if work[i_other][0] == OK:
                        work[i] = (OK, data ^ work[i_other][1])
                        changed = True

        return [x[1] for x in work]

    def _harden(self, bits):
        bits = self._xor_nums(bits, bits[:-11])
        bits = self._xor_nums(bits, self._and_nums(bits[7:] + [0] * 7, self._to_bitarray(0x2B5B2500)))
        bits = self._xor_nums(bits, self._and_nums(bits[15:] + [0] * 15, self._to_bitarray(0xDB8B0000)))
        bits = self._xor_nums(bits, bits[:-18])
        return bits

    def _harden_inverse(self, bits):
        # inverse for: bits = _xor_nums(bits, bits[:-11])
        bits = self._xor_nums(bits, bits[:-18])
        # inverse for: bits = _xor_nums(bits, _and_nums(bits[15:] + [0] * 15 , _to_bitarray(0xefc60000)))
        bits = self._decode_harden_midop(bits, self._to_bitarray(0xDB8B0000), 15)
        # inverse for: bits = _xor_nums(bits, _and_nums(bits[7:] + [0] * 7 , _to_bitarray(0x9d2c5680)))
        bits = self._decode_harden_midop(bits, self._to_bitarray(0x2B5B2500), 7)
        # inverse for: bits = _xor_nums(bits, bits[:-11])
        bits = self._xor_nums(bits, [0] * 11 + bits[:11] + [0] * 10)
        bits = self._xor_nums(bits, bits[11:21])

        return bits

    def _regen(self):
        # C code translated from python sources
        N = 25
        M = 7
        MATRIX_A = 0x8EBFD028
        LOWER_MASK = 0x7fffffff
        UPPER_MASK = 0x80000000
        mag01 = [self._to_bitarray(0), self._to_bitarray(MATRIX_A)]

        l_bits = self._to_bitarray(LOWER_MASK)
        u_bits = self._to_bitarray(UPPER_MASK)

        for kk in range(0, N - M):
            y = self._or_nums(self._and_nums(self.mt[kk], u_bits), self._and_nums(self.mt[kk + 1], l_bits))
            self.mt[kk] = self._xor_nums(self._xor_nums(self.mt[kk + M], y[:-1]), mag01[y[-1] & 1])

        for kk in range(N - M, N - 1):
            y = self._or_nums(self._and_nums(self.mt[kk], u_bits), self._and_nums(self.mt[kk + 1], l_bits))
            self.mt[kk] = self._xor_nums(self._xor_nums(self.mt[kk + (M - N)], y[:-1]), mag01[y[-1] & 1])

        y = self._or_nums(self._and_nums(self.mt[N - 1], u_bits), self._and_nums(self.mt[0], l_bits))
        self.mt[N - 1] = self._xor_nums(self._xor_nums(self.mt[M - 1], y[:-1]), mag01[y[-1] & 1])

        self.counter = 0

    def untwist(self):
        w, n, m = 32, 25, 7
        a = 0x8EBFD028

        # I like bitshifting more than these custom functions...
        MT = [self._to_int(x) for x in self.mt]

        for i in range(n-1, -1, -1):
            result = 0
            tmp = MT[i]
            tmp ^= MT[(i + m) % n]
            if tmp & (1 << w-1):
                tmp ^= a
            result = (tmp << 1) & (1 << w-1)
            tmp = MT[(i - 1 + n) % n]
            tmp ^= MT[(i + m-1) % n]
            if tmp & (1 << w-1):
                tmp ^= a
                result |= 1
            result |= (tmp << 1) & ((1 << w-1) - 1)
            MT[i] = result

        self.mt = [self._to_bitarray(x) for x in MT]

    def offset(self, n):
        if n >= 0:
            [self._predict_32() for _ in range(n)]
        else:
            [self.untwist() for _ in range(-n // 25 + 1)]
            [self._predict_32() for _ in range(25 - (-n % 25))]

    

conn = remote("91.99.1.179", 60006)

print(conn.recvuntil(b"That's why I have no problem tossing out encrypted secrets like this one: \n"))

encrytpted_flag = conn.recvline()[:-1]
print(encrytpted_flag)

samples = []

for i in range(25):
    print(conn.sendlineafter(b"Enter hex string: ", b"00000000"))
    sample = conn.recvline()[:-1].decode()
    samples.append(int(sample, 16))

print(samples)

guessr = RandGuesser()
for sample in samples:
    guessr.submit(sample)


guessr.offset(-25)
guessr.offset(-6)

encrytpted_flag = bytes.fromhex(encrytpted_flag.decode())

for i in range(len(encrytpted_flag) // 4):
    print(xor(encrytpted_flag[i*4:i*4+4], long_to_bytes(guessr.predict_getrandbits(32))).decode(), end="")

conn.interactive()