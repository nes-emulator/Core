from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


def eor_base_exec(cpu, value):
    new_calculated_value = cpu.state.a.get_value() ^ value

    new_reg_value = new_calculated_value % 256
    cpu.state.a.set_value(new_reg_value)

    cpu.state.status.zero = (new_reg_value == 0)
    cpu.state.status.negative = (new_reg_value > 127)


class EorInstructionMemoryBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)
        eor_base_exec(cpu, value)
        return address


class EorInstructionImmediateAddr(Instruction, ImmediateAddr):
    def __init__(self):
        super().__init__(opcode=0x49, cycles=2)

    def execute(self, memory, cpu, params):
        value = self.calculate_unified_parameter(params, cpu, memory)
        eor_base_exec(cpu, value)
        

class EorInstructionZeroPageAddr(Instruction, ZeroPageAddr, EorInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x45, cycles=3)


class EorInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, EorInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x55, cycles=4)


class EorInstructionAbsoluteAddr(Instruction, AbsoluteAddr, EorInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x4D, cycles=4)


class EorInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, EorInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x5D, cycles=4)


class EorInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, EorInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x59, cycles=4)


class EorInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, EorInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x41, cycles=6)


class EorInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, EorInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x51, cycles=5)
