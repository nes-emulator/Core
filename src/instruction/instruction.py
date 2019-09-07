
class Instruction(object):
    opcode = ''
    cycles = 1

    def __init__(self, opcode, cycles):
        self.opcode = opcode
        self.cycles = cycles

    def execute(self, params):
        pass

    def get_cycles(self):
        return self.cycles