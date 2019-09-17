from src.instruction.instruction import Instruction

class CLC(Instruction):
    def __init__(self):
        super().__init__(opcode=24, cycles=2)

    def execute(self, memory, cpu, params):
        cpu.state.status.carry = False

class SEC(Instruction):
    def __init__(self):
        super().__init__(opcode=56, cycles=1)

    def execute(self, memory, cpu, params):
        cpu.state.status.carry = True

class CLI(Instruction):
    def __init__(self):
        super().__init__(opcode=88, cycles=1)

    def execute(self, memory, cpu, params):
        cpu.state.status.interrupt = False

class SEI(Instruction):
    def __init__(self):
        super().__init__(opcode=120, cycles=1)

    def execute(self, memory, cpu, params):
        cpu.state.status.interrupt = True

class CLV(Instruction):
    def __init__(self):
        super().__init__(opcode=184, cycles=1)

    def execute(self, memory, cpu, params):
        cpu.state.status.overflow = False

class CLD(Instruction):
    def __init__(self):
        super().__init__(opcode=216, cycles=1)

    def execute(self, memory, cpu, params):
        cpu.state.status.decimal = False

class SED(Instruction):
    def __init__(self):
        super().__init__(opcode=248, cycles=1)

    def execute(self, memory, cpu, params):
        cpu.state.status.decimal = True

class BRK(Instruction):
    def __init__(self):
        super().__init__(opcode=0, cycles=7)

    def execute(self, memory, cpu, params):
        cpu.state.status.brk = True