from .instruction import Instruction
from .implementation import *

def _mount_all_instructions_list():
    return [ i() for i in Instruction.__subclasses__() ]

class InstructionCollection:
    all_instructions = None

    @staticmethod
    def get_instruction(opcode):
        if not InstructionCollection.all_instructions:
            InstructionCollection.all_instructions = { i.opcode: i for i in _mount_all_instructions_list() }

        return InstructionCollection.all_instructions.get(opcode, Instruction('none', 1))
