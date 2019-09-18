from src.instruction.instruction import *
from src.instruction.addressing import *

class INX(Instruction):
    def __init__(self):
        super().__init__(opcode=232, cycles=2)

    def execute(self, memory, cpu, params):
        new_calculated = cpu.state.x.get_value() + 1

        new_reg_value = new_calculated % 256
        cpu.state.x.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)

class INY(Instruction):
    def __init__(self):
        super().__init__(opcode=200, cycles=2)

    def execute(self, memory, cpu, params):
        new_calculated = cpu.state.y.get_value() + 1

        new_reg_value = new_calculated % 256
        cpu.state.y.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)

# TODO Review thsi 136
class INC(Instruction):
    def __init__(self):
        super().__init__(opcode='inc', cycles=1)

    def execute(self, memory, cpu, params):

        pass