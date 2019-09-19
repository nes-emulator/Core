from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class INX(Instruction):
    def __init__(self):
        super().__init__(opcode=232, cycles=2)

    def execute(self, memory, cpu, params):
        new_calculated = cpu.state.x.get_value() + 1

        new_reg_value = new_calculated % 256
        cpu.state.x.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)

class INY(Instruction):
    def __init__(self):
        super().__init__(opcode=200, cycles=2)

    def execute(self, memory, cpu, params):
        new_calculated = cpu.state.y.get_value() + 1

        new_reg_value = new_calculated % 256
        cpu.state.y.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)

class INCBaseInstruction(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)

        new_calculated_value = value + 1
        memory_value = new_calculated_value % 256

        memory.set_content(address, memory_value)

        cpu.state.status.zero = (memory_value == 0)
        cpu.state.status.negative = (memory_value > 127)


class INCZeroPageAddr(Instruction, ZeroPageAddr, INCBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xE6, cycles=5)

class INCZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, INCBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xF6, cycles=6)

class INCAbsoluteAddr(Instruction, AbsoluteAddr, INCBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xEE, cycles=6)

class INCAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, INCBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xFE, cycles=7)