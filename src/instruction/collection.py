from .instruction import Instruction
from .implementation import *

def _mount_all_instructions_list():
    instructions = [ i() for i in Instruction.__subclasses__() ]
    coded_instructions = [None] * 256

    for i in instructions:
        coded_instructions[i.opcode] = i

    return coded_instructions

class InstructionCollection:
    all_instructions = None

    @staticmethod
    def initialize():
        InstructionCollection.all_instructions = _mount_all_instructions_list()

    @staticmethod
    def get_instruction(opcode):
        if not InstructionCollection.all_instructions:
            InstructionCollection.initialize()

        return InstructionCollection.all_instructions[opcode] or Instruction('none', 1)
