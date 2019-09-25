from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class Nop(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0xEA, cycles = 2)

    def execute(self, memory, cpu, params):
        pass
