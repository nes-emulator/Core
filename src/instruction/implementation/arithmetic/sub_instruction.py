from src.instruction.instruction import Instruction
from src.instruction.addressing import *
from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


class SubInstructionBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        carry_sub = 0 if cpu.state.status.carry else 1

        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)

        old_reg_value = cpu.state.a.get_value()
        new_calculated_value = cpu.state.a.get_value() - value - carry_sub

        new_reg_value = new_calculated_value if (new_calculated_value >= 0) else (256 - abs(new_calculated_value))
        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)
        cpu.state.status.overflow = (old_reg_value ^ new_calculated_value) & 0x80 != 0 and (old_reg_value ^ value) & 0x80 != 0

        if (cpu.state.status.decimal and (old_reg_value & 0xf) - carry_sub < (value & 0xf)):
            new_calculated_value -= 6

        if (cpu.state.status.decimal and new_calculated_value > 0x99):
            new_calculated_value -= 0x60

        new_reg_value = new_calculated_value if (new_calculated_value >= 0) else (256 - abs(new_calculated_value))
        cpu.state.a.set_value(new_reg_value)
        cpu.state.status.carry = (new_calculated_value >= 0)

class SubInstructionImmediateAddr(Instruction, ImmediateAddr, SubInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xE9, cycles=2)

class SubInstructionZeroPageAddr(Instruction, ZeroPageAddr, SubInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xE5, cycles=3)

class SubInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, SubInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xF5, cycles=1)

class SubInstructionAbsoluteAddr(Instruction, AbsoluteAddr, SubInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xED, cycles=1)

class SubInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, SubInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xFD, cycles=1)

class SubInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, SubInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xF9, cycles=1)

class SubInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, SubInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xE1, cycles=1)

class SubInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, SubInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xF1, cycles=1)
