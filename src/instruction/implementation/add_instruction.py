from ..instruction import Instruction
from ..result import InstructionResult

class AddInstruction(Instruction):

    def __init__(self):
        super().__init__('add', 1)

    def execute(self, params):
        result = InstructionResult()
        result.set_a_reg(0)
        return result