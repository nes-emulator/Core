from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class Nop(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0xEA, cycles = 2)


class Nop04(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x04, cycles = 2)


class Nop14(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x14, cycles = 2)


class Nop34(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x34, cycles = 2)


class Nop44(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x44, cycles = 2)


class Nop54(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x54, cycles = 2)


class Nop64(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x64, cycles = 2)


class Nop74(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x74, cycles = 2)


class NopD4(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0xD4, cycles = 2)


class NopF4(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0xF4, cycles = 2)


class Nop1A(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0x1A, cycles = 2)


class Nop3A(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0x3A, cycles = 2)


class Nop5A(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0x5A, cycles = 2)


class Nop7A(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0x7A, cycles = 2)


class NopDA(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0xDA, cycles = 2)


class NopFA(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0xFA, cycles = 2)


class Nop0C(Instruction, ImpliedAddr):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0x0C, cycles = 2)


class Nop1C(Instruction, ImpliedAddr):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0x1C, cycles = 2)


class Nop3C(Instruction, ImpliedAddr):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0x3C, cycles = 2)


class Nop5C(Instruction, ImpliedAddr):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0x5C, cycles = 2)


class Nop7C(Instruction, ImpliedAddr):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0x7C, cycles = 2)


class NopDC(Instruction, ImpliedAddr):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0xDC, cycles = 2)


class NopFC(Instruction, ImpliedAddr):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0xFC, cycles = 2)


class Nop80(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x80, cycles = 2)
