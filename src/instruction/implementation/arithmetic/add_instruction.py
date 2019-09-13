from src.instruction.instruction import Instruction
from src.instruction.result import InstructionResult
from src.instruction.addressing import *


class AddInstruction(Instruction):
    included_addr_modes = {69: ImmediateAddr, 65: ZeroPageAddr, 75: ZeroPgDirectIndexedRegXAddr, 60: AbsoluteAddr,
                           70: AbsDirectIndexedRegXAddr, 79: AbsDirectIndexedRegYAddr, 61: IndirectPreIndexedAddr,
                           71: IndirectPostIndexedAddr}

    def __init__(self, opcode, addressing):
        super().__init__(opcode, 1)  # fix cycles
        self.addressing = addressing

    def execute(self, params):
        result = InstructionResult()
        result.set_a_reg(0)
        return result
