from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class BranchBaseInstruction(CalculateAddress):
    def branch(self, memory, cpu, params, branch_flag):
        branch_pos = params[0]
        signed_pos_offset = branch_pos if branch_pos < 128 else (~(255 - branch_pos) + 1)

        if branch_flag:
            cpu.state.pc.set_value(cpu.state.pc.get_value() + signed_pos_offset)

class BCC(Instruction, ImmediateAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x90, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, not cpu.state.status.carry)

class BCS(Instruction, ImmediateAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xB0, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, cpu.state.status.carry)

class BEQ(Instruction, ImmediateAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xF0, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, cpu.state.status.zero)

class BMI(Instruction, ImmediateAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x30, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, cpu.state.status.negative)

class BNE(Instruction, ImmediateAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xD0, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, not cpu.state.status.zero)

class BPL(Instruction, ImmediateAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x10, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, not cpu.state.status.negative)

class BVC(Instruction, ImmediateAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x50, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, not cpu.state.status.overflow)

class BVS(Instruction, ImmediateAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x70, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, cpu.state.status.overflow)


