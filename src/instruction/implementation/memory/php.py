from src.instruction.instruction import *
from src.instruction.addressing.addressing import ImpliedAddr
from src.register.statusregister import StatusRegister


class Php(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode=0x8, cycles=3)

    def execute(self, memory, cpu, params):

        # get a copy of status register, but with BRK set
        stat = StatusRegister(cpu.state.status.to_val())
        stat.brk = True
        stat.unused = True
        # push the copy
        memory.stack.push_val(stat.to_val())
        return memory.solve_mirroring(memory.stack.get_top() + 1)
