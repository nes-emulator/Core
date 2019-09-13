from src.instruction.instruction import *
from src.instruction.addressing import *

class AddInstructionBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        return address

class AddInstructionImmediateAddr(Instruction, ImmediateAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(69, 1)

class AddInstructionZeroPageAddr(Instruction, ZeroPageAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(65, 1)

class AddInstructionZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(75, 1)

class AddInstructionAbsoluteAddr(Instruction, AbsoluteAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(60, 1)

class AddInstructionAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(70, 1)

class AddInstructionAbsDirectIndexedRegYAddr(Instruction, AbsDirectIndexedRegYAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(79, 1)

class AddInstructionIndirectPreIndexedAddr(Instruction, IndirectPreIndexedAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(61, 1)

class AddInstructionIndirectPostIndexedAddr(Instruction, IndirectPostIndexedAddr, AddInstructionBase):
    def __init__(self):
        super().__init__(71, 1)
