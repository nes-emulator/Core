from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


class AndInstructionBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)

        new_calculated_value = cpu.state.a.get_value() & value

        new_reg_value = new_calculated_value % 256
        cpu.state.a.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)


class AndInstructionImmediateAddr(Instruction, ImmediateAddr, AndInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x29, cycles=2)

class AndInstructionZeroPageAddr(Instruction, ZeroPageAddr, AndInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x25, cycles=3)

class AndInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, AndInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x35, cycles=4)

class AndInstructionAbsoluteAddr(Instruction, AbsoluteAddr, AndInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x2D, cycles=4)

class AndInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, AndInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x3D, cycles=4)

class AndInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, AndInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x39, cycles=4)

class AndInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, AndInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x21, cycles=6)

class AndInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, AndInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x31, cycles=5)
