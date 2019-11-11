from src.register.register import Register
from src.util.util import *

class DmcChannel:

    def __init__(self, first, second, third, fourth):
        self.control = Register(first)
        self.direct_load = Register(second)
        self.sample_addr = Register(third)
        self.sample_len = Register(fourth)

    ## Control ($4010)
    def get_irq_enable(self):
        return self.control.get_bit(7)

    def get_loop_sample(self):
        return self.control.get_bit(6)

    def get_frequency_idx(self):
        return flags_to_val_low(self.control.get_bits(0, 4))

    ## Direct Load ($4011)
    def get_direct_load(self):
        return flags_to_val_low(self.direct_load.get_bits(0, 7))

    ## Sample Address ($4012)
    def get_sample_addr(self):
        return self.sample_addr.get_value()

    ## Sample Length ($4013)
    def get_sample_len(self):
        return self.sample_len.get_value()
