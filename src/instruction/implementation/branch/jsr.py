from src.instruction.instruction import *
from src.util.util import apply_mask
from src.instruction.addressing.addressing import AbsoluteAddr


class Jsr(Instruction, AbsoluteAddr):
    def execute(self, memory, cpu, params):
        pc_val = cpu.state.pc.get_value()
        cpu.state.pc.set_value(pc_val - 1)
        pc_initial_pos = memory.stack.get_top()
        memory.stack.push_pc()
        new_pc = self.calculate_unified_parameter(params, cpu, memory)
        cpu.state.pc.set_value(new_pc)
        return pc_initial_pos

    def __init__(self):
        super().__init__(opcode=0x20, cycles=6)
