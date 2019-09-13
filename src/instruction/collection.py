from .instruction import Instruction
from .implementation import *

def _mount_all_instructions():
    instructions = {}
    for instruction in Instruction.__subclasses__():
        for opcode, addr_mode in instruction.included_addr_modes.items():
            instructions[opcode] = instruction(opcode, addr_mode)
    return instructions


class InstructionCollection:
    all_instructions = _mount_all_instructions()

    @staticmethod
    def get_instruction(opcode):
        return InstructionCollection.all_instructions.get(opcode, Instruction('none', 1))
