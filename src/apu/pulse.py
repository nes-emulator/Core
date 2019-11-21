from src.register.register import Register
from src.util.util import *

class PulseChannel:

    def __init__(self, first, second, third, fourth):
        self.control = Register(first)
        self.sweep = Register(second)
        self.timer_low = Register(third)
        self.length_timer = Register(fourth)

    ## Parsing control bits (ADDR 4000 or 4004)
    def set_duty(self, val):
        bits = extract_bits(val)
        self.control.change_bits(6, bits)

    def get_duty(self):
        return self.control.get_bit(7) * 2 + self.control.get_bit(6)

    def set_loop_envelope(self, val):
        self.control.change_bit(5, val)

    def get_loop_envelope(self):
        return self.control.get_bit(5)

    def set_volume(self, val):
        self.control.change_bit(4, val)

    def get_volume(self):
        return self.control.get_value() & 0b00001111

    # 4-bit value
    def set_envelope_period(self, val):
        bits = extract_bits(val)
        self.control.change_bits(0, bits)

    def get_envelope_period(self):
        return flags_to_val_low(self.control.get_bits(0, 4))

    ## Parsing Sweep Unit (4001 or 4005)
    def get_sweep_enabled(self):
        return self.sweep.get_bit(7)

    def set_sweep_enabled(self, val):
        self.sweep.change_bit(7, val)

    def get_period(self):
        return flags_to_val_low(self.sweep.get_bits(4, 3))

    def set_period(self, bits):
        self.sweep.change_bits(4, bits)

    def get_negative(self):
        return self.sweep.get_bit(3)

    def set_negative(self, val):
        self.sweep.change_bit(3, val)

    def get_shift_count(self):
        return flags_to_val_low(self.sweep.get_bits(0, 3))

    def set_shift_count(self, bits):
        self.sweep.change_bits(0, bits)

    ## Parsing timer low
    def get_timer_low(self):
        return self.timer_low.get_value()

    def set_timer_low(self, val):
        self.timer_low.set_value(val)

    ## Parsing LCL and timer high
    def set_timer_high(self, val):
        bits = extract_bits(val)
        self.length_timer.change_bits(0, bits)

    def get_timer_high(self):
        return flags_to_val_low(self.length_timer.get_bits(0, 3))

    def set_lcl(self, val):
        bits = extract_bits(val)
        self.length_timer.change_bits(3, bits)

    def get_lcl(self):
        return flags_to_val_low(self.length_timer.get_bits(3, 5))
