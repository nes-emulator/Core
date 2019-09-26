from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class DEX(Instruction):
    def __init__(self):
        super().__init__(opcode=202, cycles=2)

    def execute(self, memory, cpu, params):
        new_calculated = cpu.state.x.get_value() - 1

        new_reg_value = new_calculated if (new_calculated >= 0) else (256 - abs(new_calculated))
        cpu.state.x.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)

class DEY(Instruction):
    def __init__(self):
        super().__init__(opcode=136, cycles=2)

    def execute(self, memory, cpu, params):
        new_calculated = cpu.state.y.get_value() - 1

        new_reg_value = new_calculated if (new_calculated >= 0) else (256 - abs(new_calculated))
        cpu.state.y.set_value(new_reg_value)

        cpu.state.status.zero = (new_reg_value == 0)
        cpu.state.status.negative = (new_reg_value > 127)

class DECBaseInstruction(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        address = self.calculate_unified_parameter(params, cpu, memory)
        value = self.retrieve_address_data(memory, address)

        new_calculated_value = value - 1
        memory_value = new_calculated_value if (new_calculated_value >= 0) else (256 - abs(new_calculated_value))

        memory.set_content(address, memory_value)

        cpu.state.status.zero = (memory_value == 0)
        cpu.state.status.negative = (memory_value > 127)

        return address


class DECZeroPageAddr(Instruction, ZeroPageAddr, DECBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xC6, cycles=5)

class DECZeroPgDirectIndexedRegXAddr(Instruction, ZeroPgDirectIndexedRegXAddr, DECBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xD6, cycles=6)

class DECAbsoluteAddr(Instruction, AbsoluteAddr, DECBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xCE, cycles=6)

class DECAbsDirectIndexedRegXAddr(Instruction, AbsDirectIndexedRegXAddr, DECBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xDE, cycles=7)