from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class JumpBaseInstruction(CalculateAddress):
    def branch(self, memory, cpu, params, branch_flag):
        address = self.calculate_unified_parameter(params, cpu, memory)
        jump_position = self.retrieve_address_data(memory, address)
        cpu.state.pc.set_value(jump_position)
        exit(0) ### TODO REVIEW JUMP INSTRUCTION

class JMPAbsolute(Instruction, AbsoluteAddr, JumpBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x4C, cycles=3)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, True)

class JMPIndirect(Instruction, IndirectAddr, JumpBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x6C, cycles=5)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, True)

