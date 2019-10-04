from src.instruction.instruction import *
from src.instruction.addressing.addressing import *

class BranchBaseInstruction(CalculateAddress):
    def branch(self, memory, cpu, params, branch_flag):
        if branch_flag:
            cpu.cycles += 1

            branch_pos = self.calculate_unified_parameter(params, cpu, memory)
            signed_pos_offset = branch_pos if branch_pos < 128 else (~(255 - branch_pos))

            cpu.state.pc.set_value(cpu.state.pc.get_value() + signed_pos_offset)

class BCC(Instruction, RelativeIndexedAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x90, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, not cpu.state.status.carry)

class BCS(Instruction, RelativeIndexedAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xB0, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, cpu.state.status.carry)

class BEQ(Instruction, RelativeIndexedAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xF0, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, cpu.state.status.zero)

class BMI(Instruction, RelativeIndexedAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x30, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, cpu.state.status.negative)

class BNE(Instruction, RelativeIndexedAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0xD0, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, not cpu.state.status.zero)

class BPL(Instruction, RelativeIndexedAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x10, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, not cpu.state.status.negative)

class BVC(Instruction, RelativeIndexedAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x50, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, not cpu.state.status.overflow)

class BVS(Instruction, RelativeIndexedAddr, BranchBaseInstruction):
    def __init__(self):
        super().__init__(opcode=0x70, cycles=2)

    def execute(self, memory, cpu, params):
        self.branch(memory, cpu, params, cpu.state.status.overflow)
