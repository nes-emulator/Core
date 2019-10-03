from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


def compare_base(cpu, value, base_reg_value):
    new_calculated = base_reg_value - value
    new_reg_value = new_calculated if (new_calculated >= 0) else (256 - abs(new_calculated))

    cpu.state.status.zero = (new_reg_value == 0)
    cpu.state.status.carry = (new_calculated >= 0)
    cpu.state.status.negative = (new_reg_value > 127)


class CPXBaseMemoryInstruction(Executable, CalculateAddress):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)
        compare_base(cpu, value, cpu.state.x.get_value())
        return memory.solve_mirroring(address)


class CPXImmediateAddr(Instruction, ImmediateAddr):
    def __init__(self):
        super().__init__(opcode=0xE0, cycles=2)

    def execute(self, memory, cpu, params):
        value = self.calculate_unified_parameter(params, cpu, memory)
        compare_base(cpu, value, cpu.state.x.get_value())


class CPXZeroPageAddr(Instruction, ZeroPageAddr, CPXBaseMemoryInstruction):
    def __init__(self):
        super().__init__(opcode=0xE4, cycles=3)


class CPXAbsoluteAddr(Instruction, AbsoluteAddr, CPXBaseMemoryInstruction):
    def __init__(self):
        super().__init__(opcode=0xEC, cycles=4)


class CPYBaseMemoryInstruction(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)
        compare_base(cpu, value, cpu.state.y.get_value())
        return memory.solve_mirroring(address)


class CPYImmediateAddr(Instruction, ImmediateAddr):
    def __init__(self):
        super().__init__(opcode=0xC0, cycles=2)

    def execute(self, memory, cpu, params):
        value = self.calculate_unified_parameter(params, cpu, memory)
        compare_base(cpu, value, cpu.state.y.get_value())


class CPYZeroPageAddr(Instruction, ZeroPageAddr, CPYBaseMemoryInstruction):
    def __init__(self):
        super().__init__(opcode=0xC4, cycles=3)


class CPYAbsoluteAddr(Instruction, AbsoluteAddr, CPYBaseMemoryInstruction):
    def __init__(self):
        super().__init__(opcode=0xCC, cycles=4)


class CMPInstructionMemoryBase(Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)
        compare_base(cpu, value, cpu.state.a.get_value())
        return memory.solve_mirroring(address)


class CMPInstructionImmediateAddr(Instruction, ImmediateAddr):
    def __init__(self):
        super().__init__(opcode=0xC9, cycles=2)

    def execute(self, memory, cpu, params):
        value = self.calculate_unified_parameter(params, cpu, memory)
        compare_base(cpu, value, cpu.state.a.get_value())


class CMPInstructionZeroPageAddr(Instruction, ZeroPageAddr, CMPInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xC5, cycles=3)


class CMPInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, CMPInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xD5, cycles=1)


class CMPInstructionAbsoluteAddr(Instruction, AbsoluteAddr, CMPInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xCD, cycles=1)


class CMPInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, CMPInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xDD, cycles=1)


class CMPInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, CMPInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xD9, cycles=1)


class CMPInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, CMPInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xC1, cycles=1)


class CMPInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, CMPInstructionMemoryBase):
    def __init__(self):
        super().__init__(opcode=0xD1, cycles=1)
