from sympy.physics.quantum import TensorProduct
from sympy import Matrix, sqrt

# Gates
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

def decode(state, prev):
    # Determine the encoded bits based on the gates applied to the previous state (superdense coding)
    if prev == state:
        return "00"
    elif TensorProduct(X, I) * prev == state:
        return "01"
    elif TensorProduct(Z, I) * prev == state:
        return "10"
    else:
        return "11"

def main():
    with open("out.txt", "r") as f:
        # Initial Bell state (Φ+, Φ-, Ψ+ or Ψ-)
        prev_state = eval(f.readline())
        
        digest = ""
        for line in f:
            state = eval(line)
            digest += decode(state, prev_state)
            # Alice keeps the quantic state for the future gates
            prev_state = state
    
    # Decode from binary
    n = int('0b'+digest,2)
    print(n.to_bytes((n.bit_length() + 7)//8,'big').decode())
    
if __name__ == "__main__":
    main()