from src.register.register import Register
from src.util.util import *

class TriangleChannel:

    def __init__(self, first, second, third):
        self.control = Register(first)
        self.timer_low = Register(second)
        self.length_timer = Register(third)

    ## Control ($4008)
    def get_counter_control(self):
        return self.control.get_bit(7)

    def get_linear_counter(self):
        bits = self.control.get_bits(0, 7)
        return flags_to_val_low(bits)

    ## Timer Low ($400A)
    def get_timer_low(self):
        return self.timer_low.get_value()

    ## LCL, Timer High ($400B)
    def get_timer_high(self):
        bits = self.length_timer.get_bits(0, 3)
        return flags_to_val_low(bits)

    def get_lcl(self):
        bits = self.length_timer.get_bits(3, 5)
        return flags_to_val_low(bits)
