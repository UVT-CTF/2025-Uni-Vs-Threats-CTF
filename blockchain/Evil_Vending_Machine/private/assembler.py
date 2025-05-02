from pyevmasm import assemble_hex

evm_code = '''PUSH2 0x951d
    PUSH4 0x6063eb0c
    DIV
    PUSH2 0x3b83
    CALLVALUE
    PUSH1 0x63
    PUSH2 0x3f72
    PUSH1 0xb4
    ADDMOD
    MUL
    SUB
    PUSH1 0x2c
    PUSH2 0x1af3
    MUL
    PUSH2 0x7a4
    MSTORE
    PUSH3 0x7d0b9
    PUSH2 0xab52
    ADD
    PUSH2 0x7c7
    MSTORE
    PUSH3 0x26a85
    PUSH2 0x952d
    XOR
    PUSH3 0x881ba
    MSTORE
    PUSH2 0x7c7
    MLOAD
    PUSH2 0x7a4
    MLOAD
    MUL
    EQ
    PUSH1 0x48
    JUMPI
    SELFDESTRUCT
    STOP
'''
bytecode = assemble_hex(evm_code)
print(bytecode)
