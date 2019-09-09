from ..instruction import Instruction
from ..result import InstructionResult

class SubInstruction(Instruction):

    def __init__(self):
        super().__init__('sub', 2)

    def execute(self, params):
        result = InstructionResult()
        result.set_x_reg(0)
        return result