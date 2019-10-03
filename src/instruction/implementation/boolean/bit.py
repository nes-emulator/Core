from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


class BitInstructionBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)

        new_reg_value = cpu.state.a.get_value() & value

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (value > 127)
        cpu.state.status.overflow = (value & 0x40 != 0)

        return memory.solve_mirroring(address)


class BitInstructionZeroPageAddr(Instruction, ZeroPageAddr, BitInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x24, cycles=3)


class BitInstructionAbsoluteAddr(Instruction, AbsoluteAddr, BitInstructionBase):
    def __init__(self):
        super().__init__(opcode=0x2C, cycles=4)
