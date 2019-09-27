from src.instruction.instruction import *


class Php(Instruction):
    def __init__(self):
        super().__init__(opcode=0x8, cycles=3)

    def execute(self, memory, cpu, params):
        memory.stack.push_val(cpu.state.status.to_val())
        return memory.stack.get_top() + 1
