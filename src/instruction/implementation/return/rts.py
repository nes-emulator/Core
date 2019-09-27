from src.instruction.instruction import *
from src.instruction.addressing.addressing import ImpliedAddr


class Rts(Instruction, ImpliedAddr):
    def execute(self, memory, cpu, params):
        memory.stack.pop_pc()
        pc_val = cpu.state.pc.get_value()
        cpu.state.pc.set_value(pc_val + 1)

    def __init__(self):
        super().__init__(opcode=0x60, cycles=6)
