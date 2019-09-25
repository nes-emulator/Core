from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class LoadX(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        # X <- M
        val = self.retrieve_address_data(memory, addr)
        cpu.state.x.set_value(val)

        # update status register
        cpu.state.status.zero = (val == 0)
        cpu.state.status.negative = (val > 127)

class LdxImmediate(Instruction, ImmediateAddr, LoadX):
    def __init__(self):
        super().__init__(opcode = 0xA2, cycles = 2)

class LdxImmediate(Instruction, ZeroPageAddr, LoadX):
    def __init__(self):
        super().__init__(opcode = 0xA6, cycles = 3)

class LdxImmediate(Instruction, ZeroPgDirectIndexedRegYAddr, LoadX):
    def __init__(self):
        super().__init__(opcode = 0xB6, cycles = 4)

class LdxImmediate(Instruction, AbsoluteAddr, LoadX):
    def __init__(self):
        super().__init__(opcode = 0xAE, cycles = 4)

class LdxImmediate(Instruction, AbsDirectIndexedRegYAddr, LoadX):
    def __init__(self):
        super().__init__(opcode = 0xBE, cycles = 4)

class LoadY(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        # Y <- M
        val = self.retrieve_address_data(memory, addr)
        cpu.state.y.set_value(val)

        # update status register
        cpu.state.status.zero = (val == 0)
        cpu.state.status.negative = (val > 127)

class LdyImmediate(Instruction, ImmediateAddr, LoadY):
    def __init__(self):
        super().__init__(opcode = 0xA0, cycles = 2)

class LdyZeroPage(Instruction, ZeroPageAddr, LoadY):
    def __init__(self):
        super().__init__(opcode = 0xA4, cycles = 3)

class LdyZeroPageX(Instruction, ZeroPgDirectIndexedRegXAddr, LoadY):
    def __init__(self):
        super().__init__(opcode = 0xB4, cycles = 4)

class LdyAbsolute(Instruction, AbsoluteAddr, LoadY):
    def __init__(self):
        super().__init__(opcode = 0xAC, cycles = 4)

class LdyAbsoluteX(Instruction, AbsDirectIndexedRegXAddr, LoadY):
    def __init__(self):
        super().__init__(opcode = 0xBC, cycles = 4)
