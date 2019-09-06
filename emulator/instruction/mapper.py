from .instruction import Instruction

def _mount_all_instructions_list():
    ## TODO GENERIC WAY OF GETTING ALL IMPLETATED INSTUCTIONS
    return [Instruction(1, 1)]

class InstructionMapper:
    all_instructions = { i.opcode: i for i in _mount_all_instructions_list() }

    @staticmethod
    def get_instruction(opcode):
        return InstructionMapper.all_instructions[opcode] or InstructionMapper.all_instructions['none']