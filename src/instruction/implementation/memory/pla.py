from src.instruction.instruction import *


class Pla(Instruction):
    def __init__(self):
        super().__init__(opcode=0x68, cycles=4)

    def execute(self, memory, cpu, params):
        a_reg_val = memory.stack.pop_val()
        cpu.state.a.set_value(a_reg_val)

