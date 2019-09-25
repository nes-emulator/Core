from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class Tax(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0xAA, cycles = 2)

    def execute(self, memory, cpu, params):
        # A -> X
        a = cpu.state.a.get_value()
        cpu.state.x.set_value(a)

        # update status register
        cpu.state.status.zero = (a == 0)
        cpu.state.status.negative = (a > 127)

class Tay(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0xA8, cycles = 2)

    def execute(self, memory, cpu, params):
        # A -> Y
        a = cpu.state.a.get_value()
        cpu.state.y.set_value(a)

        # update status register
        cpu.state.status.zero = (a == 0)
        cpu.state.status.negative = (a > 127)

class Tsx(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0xBA, cycles = 2)

    def execute(self, memory, cpu, params):
        # SP -> X
        sp = cpu.state.sp.get_value()
        cpu.state.x.set_value(sp)

        # update status register
        cpu.state.status.zero = (sp == 0)
        cpu.state.status.negative = (sp > 127)

class Txa(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0x8A, cycles = 2)

    def execute(self, memory, cpu, params):
        # X -> A
        x = cpu.state.x.get_value()
        cpu.state.a.set_value(x)

        # update status register
        cpu.state.status.zero = (x == 0)
        cpu.state.status.negative = (x > 127)

class Txs(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0x9A, cycles = 2)

    def execute(self, memory, cpu, params):
        # X -> SP
        x = cpu.state.x.get_value()
        cpu.state.sp.set_value(x)

class Tya(Instruction, ImpliedAddr):
    def __init__(self):
        super().__init__(opcode = 0x98, cycles = 2)

    def execute(self, memory, cpu, params):
        # A <- Y
        y = cpu.state.y.get_value()
        cpu.state.a.set_value(y)

        # update status register
        cpu.state.status.zero = (y == 0)
        cpu.state.status.negative = (y > 127)
