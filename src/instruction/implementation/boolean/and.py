from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


def and_base_exec(cpu, value):
    new_calculated_value = cpu.state.a.get_value() & value

    new_reg_value = new_calculated_value % 256
    cpu.state.a.set_value(new_reg_value)

    cpu.state.status.zero = (new_reg_value == 0)
    cpu.state.status.negative = (new_reg_value > 127)


class AndInstructionMemoryBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)
        and_base_exec(cpu, value)
        return address


class AndInstructionImmediateAddr(Instruction, ImmediateAddr):
    def __init__(self):
        super().__init__(opcode=0x29, cycles=2)

    def execute(self, memory, cpu, params):
        value = self.calculate_unified_parameter(params, cpu, memory)
        and_base_exec(cpu, value)


class AndInstructionZeroPageAddr(Instruction, ZeroPageAddr, AndInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x25, cycles=3)


class AndInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, AndInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x35, cycles=4)


class AndInstructionAbsoluteAddr(Instruction, AbsoluteAddr, AndInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x2D, cycles=4)


class AndInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, AndInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x3D, cycles=4)


class AndInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, AndInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x39, cycles=4)


class AndInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, AndInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x21, cycles=6)


class AndInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, AndInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0x31, cycles=5)
