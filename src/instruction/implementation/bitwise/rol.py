from src.instruction.instruction import *
from src.instruction.addressing.addressing import *
from src.util.util import apply_mask, is_negative
from src.memory.memory import Memory


def base_calculation(num, cpu):
    num = num << 1
    if (cpu.state.status.carry):
        num = num | 1
    cpu.state.status.carry = (num > 0XFF)
    num = apply_mask(num, 0XFF)
    cpu.state.status.negative = is_negative(num, Memory.WORD_SIZE)
    cpu.state.status.zero = (num == 0)
    return num


class RolMemory(Executable, CalculateAddress):
    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        num = memory.retrieve_content(addr)
        num = base_calculation(num, cpu)
        memory.set_content(addr, num)
        return addr


class RolAccumulator(Instruction, AccumulatorAddr, CalculateAddress):
    def execute(self, memory, cpu, params):
        val_reg_a = self.calculate_unified_parameter(params, cpu, memory)
        val_reg_a = base_calculation(val_reg_a, cpu)
        cpu.state.a.set_value(val_reg_a)

    def __init__(self):
        super().__init__(opcode=0x2A, cycles=2)


class RolZeroPg(Instruction, ZeroPageAddr, RolMemory):
    def __init__(self):
        super().__init__(opcode=0x26, cycles=5)


class RolZeroPgXIndexed(Instruction, ZeroPgDirectIndexedRegXAddr, RolMemory):
    def __init__(self):
        super().__init__(opcode=0x36, cycles=6)


class RolAbsolute(Instruction, AbsoluteAddr, RolMemory):
    def __init__(self):
        super().__init__(opcode=0x2E, cycles=6)


class RolAbsoluteXIndexed(Instruction, AbsDirectIndexedRegXAddr, RolMemory):
    def __init__(self):
        super().__init__(opcode=0x3E, cycles=7)
