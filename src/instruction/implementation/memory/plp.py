from src.instruction.instruction import *
from src.register.statusregister import StatusRegister


class Plp(Instruction):
    def __init__(self):
        super().__init__(opcode=0x28, cycles=4)

    def execute(self, memory, cpu, params):
        status_val = memory.stack.pop_val()
        cpu.state.status = StatusRegister(status_val)
       