EXTERNALS flag
LOADNUM seed 0xDEADBEEF

# nextRand code (to inline)
# ADDNUM seed 0x9e3779b9
# XORSHIFT seed 16
# IMUL seed 0x21f0aaad
# XORSHIFT seed 15
# IMUL seed 0x735a2d97
# XORSHIFT seed 15

# encrypt loop setup
LOADNUM comparison 0
LOADATTRIB length flag.length
ADDNUM length -1

# encryption loop
LABEL encrypt_loop
CP i length
ADDNUM i 1

# encrypt loop body

# let shufflePos = Math.abs(nextRand() % i);
ADDNUM seed 0x9e3779b9
XORSHIFT seed 16
IMUL seed 0x21f0aaad
XORSHIFT seed 15
IMUL seed 0x735a2d97
XORSHIFT seed 15

# let temp = flag[i];
# flag[i] = flag[shufflePos];
# flag[shufflePos] = temp;
CP shuffle_pos seed
MOD shuffle_pos i
ABS shuffle_pos
SWAPARR flag shuffle_pos length

# change byte
ADDNUM seed 0x9e3779b9
XORSHIFT seed 16
IMUL seed 0x21f0aaad
XORSHIFT seed 15
IMUL seed 0x735a2d97
XORSHIFT seed 15

# flag[i] = (flag[i] ^ (nextRand() >> 2)) & 0xFF);
LOADFROMARRAY byte flag length
CP key seed
# idea: shift nextRand() based on if a debugger is detected/devtools is open
LOADNUM shift 2
LSRVAR key shift
XOR byte key
AND byte 0xFF
STORETOARRAY flag length byte

ADDNUM length -1
CMPGREATER result length comparison
JUMPIF result encrypt_loop

# finished

%FLAGCHECK%

LOADNUM retval 1
RET retval

LABEL failed
LOADNUM retval 0
RET retval