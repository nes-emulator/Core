from src.instruction.instruction import Instruction
from src.instruction.addressing import *
from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


def sub_base_exec(cpu, value):
    carry_sub = 0 if cpu.state.status.carry else 1
    old_reg_value = cpu.state.a.get_value()
    new_calculated_value = cpu.state.a.get_value() - value - carry_sub

    new_reg_value = new_calculated_value if (new_calculated_value >= 0) else (256 - abs(new_calculated_value))
    cpu.state.status.zero = (new_reg_value == 0)
    cpu.state.status.negative = (new_reg_value > 127)
    cpu.state.status.overflow = (old_reg_value ^ new_calculated_value) & 0x80 != 0 and (
            old_reg_value ^ value) & 0x80 != 0

    new_reg_value = new_calculated_value if (new_calculated_value >= 0) else (256 - abs(new_calculated_value))
    cpu.state.a.set_value(new_reg_value)
    cpu.state.status.carry = (new_calculated_value >= 0)


class SubInstructionMemoryBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)
        sub_base_exec(cpu, value)
        return address


class SubInstructionImmediateAddr(Instruction, ImmediateAddr):
    def __init__(self):
        super().__init__(opcode=0xE9, cycles=2)

    def execute(self, memory, cpu, params):
        value = self.calculate_unified_parameter(params, cpu, memory)
        sub_base_exec(cpu, value)


class SubInstructionZeroPageAddr(Instruction, ZeroPageAddr, SubInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xE5, cycles=3)


class SubInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, SubInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xF5, cycles=1)


class SubInstructionAbsoluteAddr(Instruction, AbsoluteAddr, SubInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xED, cycles=1)


class SubInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, SubInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xFD, cycles=1)


class SubInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, SubInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xF9, cycles=1)


class SubInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, SubInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xE1, cycles=1)


class SubInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, SubInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xF1, cycles=1)
