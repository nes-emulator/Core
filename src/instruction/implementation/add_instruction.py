from ..instruction import Instruction

class AddInstruction(Instruction):

    def __init__(self):
        super().__init__('add', 1)

    def execute(self, params):
        return 0