from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


class OraInstructionBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)

        new_calculated_value = cpu.state.a.get_value() | value

        new_reg_value = new_calculated_value % 256
        cpu.state.a.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)


class OraInstructionImmediateAddr(Instruction, ImmediateAddr, OraInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x09, cycles=2)

class OraInstructionZeroPageAddr(Instruction, ZeroPageAddr, OraInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x05, cycles=3)

class OraInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, OraInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x15, cycles=4)

class OraInstructionAbsoluteAddr(Instruction, AbsoluteAddr, OraInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x0D, cycles=4)

class OraInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, OraInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x1D, cycles=4)

class OraInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, OraInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x19, cycles=4)

class OraInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, OraInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x01, cycles=6)

class OraInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, OraInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x11, cycles=5)
