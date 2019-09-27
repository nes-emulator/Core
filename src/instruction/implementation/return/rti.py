from src.instruction.instruction import *
from src.instruction.addressing.addressing import ImpliedAddr
from src.register.statusregister import StatusRegister


class Rti(Instruction, ImpliedAddr):
    def execute(self, memory, cpu, params):
        src = memory.stack.pop_val()
        cpu.state.status = StatusRegister(src)
        # load return address from stack
        memory.stack.pop_pc()

    def __init__(self):
        super().__init__(opcode=0x4D, cycles=6)
