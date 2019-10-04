from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class NopParameterBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        pass


class Nop(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0xEA, cycles = 2)


class Nop04(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x04, cycles = 3)


class Nop14(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x14, cycles = 4)


class Nop34(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x34, cycles = 4)


class Nop44(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x44, cycles = 3)


class Nop54(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x54, cycles = 4)


class Nop64(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x64, cycles = 3)


class Nop74(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x74, cycles = 4)


class NopD4(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0xD4, cycles = 4)


class NopF4(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0xF4, cycles = 4)


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


class Nop0C(Instruction, AbsDirectIndexedRegXAddr):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0x0C, cycles = 4)

class Nop1C(Instruction, AbsDirectIndexedRegXAddr, NopParameterBase):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0x1C, cycles = 4)


class Nop3C(Instruction, AbsDirectIndexedRegXAddr, NopParameterBase):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0x3C, cycles = 4)


class Nop5C(Instruction, AbsDirectIndexedRegXAddr, NopParameterBase):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0x5C, cycles = 4)


class Nop7C(Instruction, AbsDirectIndexedRegXAddr, NopParameterBase):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0x7C, cycles = 4)


class NopDC(Instruction, AbsDirectIndexedRegXAddr, NopParameterBase):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0xDC, cycles = 4)


class NopFC(Instruction, AbsDirectIndexedRegXAddr, NopParameterBase):
    parameter_length = 2

    def __init__(self):
        super().__init__(opcode = 0xFC, cycles = 4)


class Nop80(Instruction, ImpliedAddr):
    parameter_length = 1

    def __init__(self):
        super().__init__(opcode = 0x80, cycles = 2)
