from src.register.register import Register
from src.util.util import *

class NoiseChannel:

    def __init__(self, first, second, third):
        self.control = Register(first)
        self.loop_period = Register(second)
        self.llc = Register(third)

    ## Control ($400C)
    def get_disable_lc(self):
        return self.control.get_bit(5)

    def get_volume(self):
        return self.control.get_bit(4)

    def get_envelope_period(self):
        return flags_to_val_low(self.control.get_bits(0, 4))

    ## Loop noise and period ($400E)
    def get_loop_noise(self):
        return self.loop_period.get_bit(7)

    def get_noise_period(self):
        return flags_to_val_low(self.control.get_bits(0, 4))

    # LCL ($400F)
    def get_lcl(self):
        return flags_to_val_low(self.control.get_bits(3, 5))
