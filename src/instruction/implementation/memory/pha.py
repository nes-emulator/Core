from src.instruction.instruction import *


class Pha(Instruction, Executable):

    def __init__(self):
        super().__init__(opcode=0x48, cycles=3)

    def execute(self, memory, cpu, params):
        memory.stack.push_val(cpu.state.a.get_value())
        return memory.stack.get_top() + 1
