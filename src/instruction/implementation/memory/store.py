from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class StoreA(CalculateAddress, Executable):

    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        memory.set_content(addr, cpu.state.a.get_value())
        return memory.solve_mirroring(addr)

class StoreX(CalculateAddress, Executable):

    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        memory.set_content(addr, cpu.state.x.get_value())
        return memory.solve_mirroring(addr)

class StoreY(CalculateAddress, Executable):

    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)
        memory.set_content(addr, cpu.state.y.get_value())
        return memory.solve_mirroring(addr)

##### STA

class StaZeroPage(Instruction, ZeroPageAddr, StoreA):
    def __init__(self):
        super().__init__(opcode = 0x85, cycles = 3)

class StaZeroPageX(Instruction, ZeroPgDirectIndexedRegXAddr, StoreA):
    def __init__(self):
        super().__init__(opcode = 0x95, cycles = 4)

class StaAbsolute(Instruction, AbsoluteAddr, StoreA):
    def __init__(self):
        super().__init__(opcode = 0x8D, cycles = 4)

class StaAbsoluteX(Instruction, AbsDirectIndexedRegXAddrNoPageCross, StoreA):
    def __init__(self):
        super().__init__(opcode = 0x9D, cycles = 5)

class StaAbsoluteY(Instruction, AbsDirectIndexedRegYAddrNoPageCross, StoreA):
    def __init__(self):
        super().__init__(opcode = 0x99, cycles = 5)

class StaIndirectX(Instruction, IndirectPreIndexedAddr, StoreA):
    def __init__(self):
        super().__init__(opcode = 0x81, cycles = 6)

class StaIndirectY(Instruction, IndirectPostIndexedAddrNoPageCross, StoreA):
    def __init__(self):
        super().__init__(opcode = 0x91, cycles = 6)

##### STX

class StxZeroPage(Instruction, ZeroPageAddr, StoreX):
    def __init__(self):
        super().__init__(opcode = 0x86, cycles = 3)

class StxZeroPageY(Instruction, ZeroPgDirectIndexedRegYAddr, StoreX):
    def __init__(self):
        super().__init__(opcode = 0x96, cycles = 4)

class StxAbsolute(Instruction, AbsoluteAddr, StoreX):
    def __init__(self):
        super().__init__(opcode = 0x8E, cycles = 4)

##### STY

class StyZeroPage(Instruction, ZeroPageAddr, StoreY):
    def __init__(self):
        super().__init__(opcode = 0x84, cycles = 3)

class StyZeroPageX(Instruction, ZeroPgDirectIndexedRegXAddr, StoreY):
    def __init__(self):
        super().__init__(opcode = 0x94, cycles = 4)

class StyAbsolute(Instruction, AbsoluteAddr, StoreY):
    def __init__(self):
        super().__init__(opcode = 0x8C, cycles = 4)
