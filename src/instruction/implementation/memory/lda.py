from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

# TODO: fix cycles when page boundaries are crossed

class LoadA(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        # A <- M
        val = memory.retrieve_content(addr)
        cpu.state.a.set_value(val)

        # update status register
        cpu.state.status.zero = (val == 0)
        cpu.state.status.negative = (val > 127)


class LdaImmediate(Instruction, ImmediateAddr, LoadA):
    def __init__(self):
        super().__init__(opcode = 0xA9, cycles = 2)

class LdaZeroPage(Instruction, ZeroPageAddr, LoadA):
    def __init__(self):
        super().__init__(opcode = 0xA5, cycles = 3)

class LdaZeroPageX(Instruction, ZeroPgDirectIndexedRegXAddr, LoadA):
    def __init__(self):
        super().__init__(opcode = 0xB5, cycles = 4)

class LdaAbsolute(Instruction, AbsoluteAddr, LoadA):
    def __init__(self):
        super().__init__(opcode = 0xAD, cycles = 4)

class LdaAbsoluteX(Instruction, AbsDirectIndexedRegXAddr, LoadA):
    def __init__(self):
        super().__init__(opcode = 0xBD, cycles = 4)

class LdaAbsoluteY(Instruction, AbsDirectIndexedRegYAddr, LoadA):
    def __init__(self):
        super().__init__(opcode = 0xB9, cycles = 4)

class LdaIndirectPre(Instruction, IndirectPreIndexedAddr, LoadA):
    def __init__(self):
        super().__init__(opcode = 0xA1, cycles = 6)

class LdaIndirectPost(Instruction, IndirectPostIndexedAddr, LoadA):
    def __init__(self):
        super().__init__(opcode = 0xB1, cycles = 5)
