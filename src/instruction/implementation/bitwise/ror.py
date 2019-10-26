from src.instruction.instruction import *
from src.instruction.addressing.addressing import *
from src.util.util import apply_mask, is_negative
from src.memory.cpu.memory import Memory


def base_calculation(num, cpu):
    if (cpu.state.status.carry):
        num = num | 0x100
    cpu.state.status.carry = bool(apply_mask(num, 0x01))
    num = num >> 1
    cpu.state.status.negative = is_negative(num, Memory.WORD_SIZE)
    cpu.state.status.zero = (num == 0)
    return num


class RorMemory(Executable, CalculateAddress):
    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        num = memory.retrieve_content(addr)
        num = base_calculation(num, cpu)
        memory.set_content(addr, num)
        return memory.solve_mirroring(addr)


class RorAccumulator(Instruction, AccumulatorAddr, CalculateAddress):
    def execute(self, memory, cpu, params):
        val_reg_a = self.calculate_unified_parameter(params, cpu, memory)
        val_reg_a = base_calculation(val_reg_a, cpu)
        cpu.state.a.set_value(val_reg_a)

    def __init__(self):
        super().__init__(opcode=0x6A, cycles=2)


class RorZeroPg(Instruction, ZeroPageAddr, RorMemory):
    def __init__(self):
        super().__init__(opcode=0x66, cycles=5)


class RorZeroPgXIndexed(Instruction, ZeroPgDirectIndexedRegXAddr, RorMemory):
    def __init__(self):
        super().__init__(opcode=0x76, cycles=6)


class RolAbsolute(Instruction, AbsoluteAddr, RorMemory):
    def __init__(self):
        super().__init__(opcode=0x6E, cycles=6)


class RorAbsoluteXIndexed(Instruction, AbsDirectIndexedRegXAddr, RorMemory):
    def __init__(self):
        super().__init__(opcode=0x7E, cycles=7)
