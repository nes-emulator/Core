
# TODO StatusRegister must extend Register if it is necessary to do arithmetic with it
class StatusRegister:

    def __init__(self):
        self.carry = 0
        self.zero = 0
        self.interrupt = 0
        self.decimal = 0
        self.overflow = 0
        self.negative = 0

    def clear(self):
        self.carry = 0
        self.zero = 0
        self.interrupt = 0
        self.decimal = 0
        self.overflow = 0
        self.negative = 0
