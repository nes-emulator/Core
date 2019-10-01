from src.instruction.instruction import *
from src.register.statusregister import StatusRegister
from src.instruction.addressing.addressing import ImpliedAddr


class Plp(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode=0x28, cycles=4)

    def execute(self, memory, cpu, params):
        status_val = memory.stack.pop_val()
        cpu.state.status = StatusRegister(status_val)
        return memory.stack.get_top() - 1