import sys
from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class JMPBase(CalculateAddress, Executable):
    def execute(self, memory, cpu, params):
        jump_position = self.calculate_unified_parameter(params, cpu, memory)
        cpu.state.pc.set_value(jump_position)

class JMPAbsolute(Instruction, AbsoluteAddr, JMPBase):
    def __init__(self):
        super().__init__(opcode=0x4C, cycles=3)

class JMPIndirect(Instruction, IndirectAddr, JMPBase):
    def __init__(self):
        super().__init__(opcode=0x6C, cycles=5)
