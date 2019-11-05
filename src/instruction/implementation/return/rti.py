from src.instruction.instruction import *
from src.instruction.addressing.addressing import ImpliedAddr
from src.register.statusregister import StatusRegister


class Rti(Instruction, ImpliedAddr):
    def execute(self, memory, cpu, params):

        status_val = memory.stack.pop_val()
        new_status = StatusRegister(status_val)

        # ignore bits 4 and 5
        new_status.brk = cpu.state.status.brk
        new_status.unused = cpu.state.status.unused
        cpu.state.status = new_status

        # load return address from stack
        memory.stack.pop_pc()

    def __init__(self):
        super().__init__(opcode=0x40, cycles=6)
