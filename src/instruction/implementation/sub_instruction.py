from ..instruction import Instruction

class SubInstruction(Instruction):

    def __init__(self):
        super().__init__('sub', 2)

    def execute(self, params):
        return 0