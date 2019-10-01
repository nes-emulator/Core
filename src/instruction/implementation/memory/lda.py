from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


# TODO: fix cycles when page boundaries are crossed
def lda_base_exec(cpu, val):
    cpu.state.a.set_value(val)

    # update status register
    cpu.state.status.zero = (val == 0)
    cpu.state.status.negative = (val > 127)


class LoadAMemory(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        val = self.retrieve_address_data(memory, addr)
        lda_base_exec(cpu, val)
        return addr


class LdaImmediate(Instruction, ImmediateAddr):
    def __init__(self):
        super().__init__(opcode=0xA9, cycles=2)

    def execute(self, memory, cpu, params):
        val = self.calculate_unified_parameter(params, cpu, memory)
        lda_base_exec(cpu, val)


class LdaZeroPage(Instruction, ZeroPageAddr, LoadAMemory):
    def __init__(self):
        super().__init__(opcode=0xA5, cycles=3)


class LdaZeroPageX(Instruction, ZeroPgDirectIndexedRegXAddr, LoadAMemory):
    def __init__(self):
        super().__init__(opcode=0xB5, cycles=4)


class LdaAbsolute(Instruction, AbsoluteAddr, LoadAMemory):
    def __init__(self):
        super().__init__(opcode=0xAD, cycles=4)


class LdaAbsoluteX(Instruction, AbsDirectIndexedRegXAddr, LoadAMemory):
    def __init__(self):
        super().__init__(opcode=0xBD, cycles=4)


class LdaAbsoluteY(Instruction, AbsDirectIndexedRegYAddr, LoadAMemory):
    def __init__(self):
        super().__init__(opcode=0xB9, cycles=4)


class LdaIndirectPre(Instruction, IndirectPreIndexedAddr, LoadAMemory):
    def __init__(self):
        super().__init__(opcode=0xA1, cycles=6)


class LdaIndirectPost(Instruction, IndirectPostIndexedAddr, LoadAMemory):
    def __init__(self):
        super().__init__(opcode=0xB1, cycles=5)
