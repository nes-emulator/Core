from src.register.register import Register
from src.util.util import *

class ApuControl:

    def __init__(self, first, second):
        self.control = Register(first)
        self.frame_counter = Register(second)

    # Control and Status ($4015)
    def get_dmc_interrupt(self):
        return self.control.get_bit(7)

    def get_frame_interrupt(self):
        return self.control.get_bit(6)

    def get_dmc_enable(self):
        return self.control.get_bit(4)

    def get_noise_lc_enable(self):
        return self.control.get_bit(3)

    def get_triangle_lc_enable(self):
        return self.control.get_bit(2)

    def get_pulse2_lc_enable(self):
        return self.control.get_bit(1)

    def get_pulse1_lc_enable(self):
        return self.control.get_bit(0)

    # Frame Counter ($4017)
    def get_frame_sequence(self):
        return self.frame_counter.get_bit(7)

    def get_disable_frame_interrupt(self):
        return self.frame_counter.get_bit(6)
