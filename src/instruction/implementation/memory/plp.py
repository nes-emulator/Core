from src.instruction.instruction import *
from src.register.statusregister import StatusRegister
from src.instruction.addressing.addressing import ImpliedAddr


class Plp(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode=0x28, cycles=4)

    def execute(self, memory, cpu, params):
        status_val = memory.stack.pop_val()
        new_status = StatusRegister(status_val)

        # ignore bits 4 and 5
        new_status.brk = cpu.state.status.brk
        new_status.unused = cpu.state.status.unused
        cpu.state.status = new_status

        return memory.solve_mirroring(memory.stack.get_top() - 1)
