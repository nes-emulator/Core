from src.instruction.instruction import *
from src.instruction.addressing.addressing import *
from src.util.util import apply_mask, is_negative
from src.memory.memory import Memory


def base_calculation(number, cpu):
    cpu.state.status.carry = bool(apply_mask(number, 0b10000000))  # the leftmost bit will be the carry
    out_number = apply_mask((number << 1), 0xFF)  # only consider bits accordingly the limit
    cpu.state.status.negative = is_negative(out_number, Memory.WORD_SIZE)
    cpu.state.status.zero = (out_number == 0)
    return out_number


class AslMemory(Executable, CalculateAddress):
    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        num = memory.retrieve_content(addr)
        num = base_calculation(num, cpu)
        memory.set_content(addr, num)
        return memory.solve_mirroring(addr)


class AslAccumulator(Instruction, AccumulatorAddr, CalculateAddress):
    def execute(self, memory, cpu, params):
        val_reg_a = self.calculate_unified_parameter(params, cpu, memory)
        val_reg_a = base_calculation(val_reg_a, cpu)
        cpu.state.a.set_value(val_reg_a)

    def __init__(self):
        super().__init__(opcode=0x0A, cycles=2)


class AslZeroPg(Instruction, ZeroPageAddr, AslMemory):
    def __init__(self):
        super().__init__(opcode=0x06, cycles=5)


class AslZeroPageXIndexed(Instruction, ZeroPgDirectIndexedRegXAddr, AslMemory):
    def __init__(self):
        super().__init__(opcode=0x16, cycles=6)


class AslAbsolute(Instruction, AbsoluteAddr, AslMemory):
    def __init__(self):
        super().__init__(opcode=0x0E, cycles=6)


class AslAbsoluteDirectX(Instruction, AbsDirectIndexedRegXAddr, AslMemory):
    def __init__(self):
        super().__init__(opcode=0x1E, cycles=7)
