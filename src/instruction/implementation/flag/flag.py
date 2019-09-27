import sys
from src.instruction.instruction import Instruction

class CLC(Instruction):
    def __init__(self):
        super().__init__(opcode=0x18, cycles=2)

    def execute(self, memory, cpu, params):
        cpu.state.status.carry = False

class SEC(Instruction):
    def __init__(self):
        super().__init__(opcode=0x38, cycles=2)

    def execute(self, memory, cpu, params):
        cpu.state.status.carry = True

class CLI(Instruction):
    def __init__(self):
        super().__init__(opcode=0x58, cycles=2)

    def execute(self, memory, cpu, params):
        cpu.state.status.interrupt = False

class SEI(Instruction):
    def __init__(self):
        super().__init__(opcode=0x78, cycles=2)

    def execute(self, memory, cpu, params):
        cpu.state.status.interrupt = True

class CLV(Instruction):
    def __init__(self):
        super().__init__(opcode=0xB8, cycles=2)

    def execute(self, memory, cpu, params):
        cpu.state.status.overflow = False

class CLD(Instruction):
    def __init__(self):
        super().__init__(opcode=0xD8, cycles=2)

    def execute(self, memory, cpu, params):
        cpu.state.status.decimal = False

class SED(Instruction):
    def __init__(self):
        super().__init__(opcode=0xF8, cycles=2)

    def execute(self, memory, cpu, params):
        cpu.state.status.decimal = True

class BRK(Instruction):
    def __init__(self):
        super().__init__(opcode=0, cycles=7)

    def execute(self, memory, cpu, params):
        cpu.state.status.brk = True
        sys.exit(0)