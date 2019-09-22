from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


class EorInstructionBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)

        new_calculated_value = cpu.state.a.get_value() ^ value

        new_reg_value = new_calculated_value % 256
        cpu.state.a.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)


class EorInstructionImmediateAddr(Instruction, ImmediateAddr, EorInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x49, cycles=2)

class EorInstructionZeroPageAddr(Instruction, ZeroPageAddr, EorInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x45, cycles=3)

class EorInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, EorInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x55, cycles=4)

class EorInstructionAbsoluteAddr(Instruction, AbsoluteAddr, EorInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x4D, cycles=4)

class EorInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, EorInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x5D, cycles=4)

class EorInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, EorInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x59, cycles=4)

class EorInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, EorInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x41, cycles=6)

class EorInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, EorInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x51, cycles=5)
