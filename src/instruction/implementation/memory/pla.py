from src.instruction.instruction import *
from src.instruction.addressing.addressing import ImpliedAddr


class Pla(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode=0x68, cycles=4)

    def execute(self, memory, cpu, params):
        a_reg_val = memory.stack.pop_val()
        cpu.state.a.set_value(a_reg_val)
        return memory.solve_mirroring(memory.stack.get_top() - 1)
