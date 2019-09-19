from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class CompareBaseInstruction(CalculateAddress):
    def compare(self, memory, cpu, params, base_reg_value):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)

        new_calculated = base_reg_value - value
        new_reg_value = new_calculated if (new_calculated >= 0) else (256 - abs(new_calculated))

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.carry = (new_calculated >= 0)
        cpu.state.status.negative = (new_reg_value > 127)

class CPXBaseInstruction(CompareBaseInstruction, Executable):
    def execute(self, memory, cpu, params):
        self.compare(memory, cpu, params, cpu.state.x.get_value())

class CPXImmediateAddr(Instruction, ImmediateAddr, CPXBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xE0, cycles=2)

class CPXZeroPageAddr(Instruction, ZeroPageAddr, CPXBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xE4, cycles=3)

class CPXAbsoluteAddr(Instruction, AbsoluteAddr, CPXBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xEC, cycles=4)



class CPYBaseInstruction(CompareBaseInstruction, Executable):
    def execute(self, memory, cpu, params):
        self.compare(memory, cpu, params, cpu.state.y.get_value())

class CPYImmediateAddr(Instruction, ImmediateAddr, CPYBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xC0, cycles=2)

class CPYZeroPageAddr(Instruction, ZeroPageAddr, CPYBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xC4, cycles=3)

class CPYAbsoluteAddr(Instruction, AbsoluteAddr, CPYBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xCC, cycles=4)




class CMPInstructionBase(CompareBaseInstruction, Executable):
    def execute(self, memory, cpu, params):
        self.compare(memory, cpu, params, cpu.state.a.get_value())

class CMPInstructionImmediateAddr(Instruction, ImmediateAddr, CMPInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xC9, cycles=2)

class CMPInstructionZeroPageAddr(Instruction, ZeroPageAddr, CMPInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xC5, cycles=3)

class CMPInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, CMPInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xD5, cycles=1)

class CMPInstructionAbsoluteAddr(Instruction, AbsoluteAddr, CMPInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xCD, cycles=1)

class CMPInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, CMPInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xDD, cycles=1)

class CMPInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, CMPInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xD9, cycles=1)

class CMPInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, CMPInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xC1, cycles=1)

class CMPInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, CMPInstructionBase):
    def __init__(self):
        super().__init__(opcode=0xD1, cycles=1)
