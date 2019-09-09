
class Instruction(object):
    opcode = ''
    cycles = 1

    def __init__(self, opcode, cycles):
        self.opcode = opcode
        self.cycles = cycles
        self.__class__ = type(self.__class__.__name__, (self.__class__,), {})
        self.__class__.__call__ = self.execute

    def execute(self, params):
        pass

    def get_cycles(self):
        return self.cycles