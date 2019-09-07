from .instruction import Instruction
from .implementation import *

def _mount_all_instructions_list():
    return [ i() for i in Instruction.__subclasses__() ]

class InstructionMapper:
    all_instructions = { i.opcode: i for i in _mount_all_instructions_list() }

    @staticmethod
    def get_instruction(opcode):
        return InstructionMapper.all_instructions.get(opcode, Instruction('none', 1))