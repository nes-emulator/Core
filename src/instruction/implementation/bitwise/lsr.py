from src.instruction.instruction import *
from src.instruction.addressing.addressing import *
from src.register.register import Register

class LSR(CalculateAddress, Executable):

    # Shift right a register by 1 and updates CPU status register
    def right_shift_register(self, reg, cpu):
        if (reg.get_value() & 0b1):
            cpu.state.status.carry = True
        else:
            cpu.state.status.carry = False

        reg.shift_right(1, False)
        cpu.state.status.zero = (reg.get_value() == 0)

    def execute(self, memory, cpu, params):
        addr = self.calculate_unified_parameter(params, cpu, memory)

        # lsr on imaginary register
        reg = Register(memory.retrieve_content(addr))
        self.right_shift_register(reg, cpu)

        # update memory
        val = reg.get_value()
        memory.set_content(addr, val)

class LsrAccumulator(Instruction, AccumulatorAddr, LSR):
    def __init__(self):
        super().__init__(opcode = 0x4A, cycles = 2)

    def execute(self, memory, cpu, params):
        self.right_shift_register(cpu.state.a, cpu)

class LsrZeroPage(Instruction, ZeroPageAddr, LSR):
    def __init__(self):
        super().__init__(opcode = 0x46, cycles = 5)

class LsrZeroPageX(Instruction, ZeroPgDirectIndexedRegXAddr, LSR):
    def __init__(self):
        super().__init__(opcode = 0x56, cycles = 6)

class LsrAbsolute(Instruction, AbsoluteAddr, LSR):
    def __init__(self):
        super().__init__(opcode = 0x4E, cycles = 6)

class LsrAbsoluteX(Instruction, AbsDirectIndexedRegXAddr, LSR):
    def __init__(self):
        super().__init__(opcode = 0x5E, cycles = 7)
