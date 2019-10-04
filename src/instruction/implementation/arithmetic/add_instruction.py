from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


def overflow(src, register, temp):
    return (not (register ^ src) & 0x80) and ((register ^ temp) & 0x80 != 0)


def add_base_exec(cpu, value):
    carry_add = 1 if cpu.state.status.carry else 0

    old_reg_value = cpu.state.a.get_value()

    new_calculated_value = old_reg_value + value + carry_add
    new_reg_value = new_calculated_value % 256
    cpu.state.a.set_value(new_reg_value)

    cpu.state.status.zero = (new_reg_value == 0)
    cpu.state.status.carry = (new_calculated_value > 255)
    cpu.state.status.negative = (new_reg_value > 127)
    cpu.state.status.overflow = overflow(value, old_reg_value, new_calculated_value)


class AddInstructionMemory(CalculateAddress, Executable):

    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        add_base_exec(cpu, memory.retrieve_content(address))
        return memory.solve_mirroring(address)


class AddInstructionImmediateAddr(Instruction, ImmediateAddr):
    def __init__(self):
        super().__init__(opcode=0x69, cycles=2)

    def execute(self, memory, cpu, params):
        value = self.calculate_unified_parameter(params, cpu, memory)
        add_base_exec(cpu, value)


class AddInstructionZeroPageAddr(Instruction, ZeroPageAddr, AddInstructionMemory):
    def __init__(self):
        super().__init__(opcode=0x65, cycles=3)


class AddInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, AddInstructionMemory):
    def __init__(self):
        super().__init__(opcode=0x75, cycles=4)


class AddInstructionAbsoluteAddr(Instruction, AbsoluteAddr, AddInstructionMemory):
    def __init__(self):
        super().__init__(opcode=0x6D, cycles=4)


class AddInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, AddInstructionMemory):
    def __init__(self):
        super().__init__(opcode=0x7D, cycles=4)


class AddInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, AddInstructionMemory):
    def __init__(self):
        super().__init__(opcode=0x79, cycles=4)


class AddInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, AddInstructionMemory):
    def __init__(self):
        super().__init__(opcode=0x61, cycles=6)


class AddInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, AddInstructionMemory):
    def __init__(self):
        super().__init__(opcode=0x71, cycles=5)
