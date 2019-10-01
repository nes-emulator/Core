from src.instruction.instruction import *
from src.instruction.addressing.addressing import *


def ldx_base_exec(cpu, val):
    cpu.state.x.set_value(val)

    # update status register
    cpu.state.status.zero = (val == 0)
    cpu.state.status.negative = (val > 127)


class LoadXMemory(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        # X <- M
        val = self.retrieve_address_data(memory, addr)
        ldx_base_exec(cpu, val)
        return addr


class LdxImmediate(Instruction, ImmediateAddr):
    def __init__(self):
        super().__init__(opcode=0xA2, cycles=2)

    def execute(self, memory, cpu, params):
        val = self.calculate_unified_parameter(params, cpu, memory)
        ldx_base_exec(cpu, val)


class LdxZeroPage(Instruction, ZeroPageAddr, LoadXMemory):
    def __init__(self):
        super().__init__(opcode=0xA6, cycles=3)


class LdxZeroPageY(Instruction, ZeroPgDirectIndexedRegYAddr, LoadXMemory):
    def __init__(self):
        super().__init__(opcode=0xB6, cycles=4)


class LdxAbsolute(Instruction, AbsoluteAddr, LoadXMemory):
    def __init__(self):
        super().__init__(opcode=0xAE, cycles=4)


class LdxAbsoluteY(Instruction, AbsDirectIndexedRegYAddr, LoadXMemory):
    def __init__(self):
        super().__init__(opcode=0xBE, cycles=4)


def ldy_base_exec(cpu, val):
    cpu.state.y.set_value(val)

    # update status register
    cpu.state.status.zero = (val == 0)
    cpu.state.status.negative = (val > 127)


class LoadYMemory(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        # Y <- M
        val = self.retrieve_address_data(memory, addr)
        ldy_base_exec(cpu, val)
        return addr


class LdyImmediate(Instruction, ImmediateAddr):
    def __init__(self):
        super().__init__(opcode=0xA0, cycles=2)

    def execute(self, memory, cpu, params):
        val = self.calculate_unified_parameter(params, cpu, memory)
        ldy_base_exec(cpu, val)


class LdyZeroPage(Instruction, ZeroPageAddr, LoadYMemory):
    def __init__(self):
        super().__init__(opcode=0xA4, cycles=3)


class LdyZeroPageX(Instruction, ZeroPgDirectIndexedRegXAddr, LoadYMemory):
    def __init__(self):
        super().__init__(opcode=0xB4, cycles=4)


class LdyAbsolute(Instruction, AbsoluteAddr, LoadYMemory):
    def __init__(self):
        super().__init__(opcode=0xAC, cycles=4)


class LdyAbsoluteX(Instruction, AbsDirectIndexedRegXAddr, LoadYMemory):
    def __init__(self):
        super().__init__(opcode=0xBC, cycles=4)
