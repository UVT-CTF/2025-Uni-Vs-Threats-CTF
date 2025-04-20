from sympy.physics.quantum import TensorProduct
from sympy import Matrix, sqrt
import random

# |0> and |1>
ket_0 = Matrix([[1], [0]])
ket_1 = Matrix([[0], [1]])

# define gates
H = (1 / sqrt(2)) * Matrix([[1, 1], [1, -1]])
CNOT = Matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])
X = Matrix([[0, 1], [1, 0]])
Z = Matrix([[1, 0], [0, -1]])
I = Matrix([[1, 0], [0, 1]])
    
# superdense encoding
def encode(state, bits):
    if(bits[1] == "1"):
        state = TensorProduct(X, I) * state
    if(bits[0] == "1"):
        state = TensorProduct(Z, I) * state
    return state

def binary(value):
    return ''.join(format(ord(i), '08b') for i in value)

# define Bell states
Phi_plus = CNOT * (TensorProduct(H * ket_0, ket_1))
Phi_minus = encode(Phi_plus, "10")
Psi_plus = encode(Phi_plus, "01")
Psi_minus = encode(Phi_plus, "11")
Bell_states = [Phi_plus, Phi_minus, Psi_plus, Psi_minus]

def main():
    state = random.choice(Bell_states)
    print("Initial state = ", state)
    
    message = "It seems that you've just cracked another challenge! A little math isn't that scary for you, is it not? Congratulations! UVT{M4st3r_0f_m4trix_mu1tip1ic4ti0n}"
    bit_stream = binary(message)
        
    for i in range(0, len(bit_stream), 2):
        bits = bit_stream[i: i+2]
        prev_state = state
        state = encode(prev_state, bits)
        print(state)
        
if __name__ == "__main__":
    main()