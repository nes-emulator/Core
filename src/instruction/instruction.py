
class Executable:
    def execute(self, memory, cpu, params):
        pass

class Instruction(Executable):
    opcode = ''
    cycles = 1

    def __init__(self, opcode, cycles):
        self.addressing = None
        self.opcode = opcode
        self.cycles = cycles
        self.__class__ = type(self.__class__.__name__, (self.__class__,), {})
        self.__class__.__call__ = self.execute

    def get_cycles(self):
        return self.cycles