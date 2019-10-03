from src.instruction.instruction import *
from src.instruction.addressing.addressing import ImpliedAddr


class Php(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode=0x8, cycles=3)

    def execute(self, memory, cpu, params):
        memory.stack.push_val(cpu.state.status.to_val())
        return memory.solve_mirroring(memory.stack.get_top() + 1)
