
# TODO StatusRegister must extend Register if it is necessary to do arithmetic with it
class StatusRegister:

    def __init__(self):
        self.carry = False
        self.zero = False
        self.interrupt = False
        self.decimal = False
        self.brk = False
        self.unused = True
        self.overflow = False
        self.negative = False

    def clear(self):
        self.carry = False
        self.zero = False
        self.interrupt = False
        self.decimal = False
        self.brk = False
        self.unused = True
        self.overflow = False
        self.negative = False
