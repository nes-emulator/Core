from src.util.util import extract_flags, flags_to_val



class StatusRegister:
    def __init__(self, val=None):
        self.clear()
        if not val is None:
            flags = extract_flags(val, 8)
            # format NV-BDIZC/
            self.negative = flags[0]
            self.overflow = flags[1]
            self.unused = flags[2]
            self.brk = flags[3]
            self.decimal = flags[4]
            self.interrupt = flags[5]
            self.zero = flags[6]
            self.carry = flags[7]

    def clear(self):
        self.carry = False
        self.zero = False
        self.interrupt = True  # IRQ   File "/home/andrietta/PycharmProjects/emulator/src/register/statusregister.py", line 2, in <module>
        self.decimal = False
        self.brk = True
        self.unused = True
        self.overflow = False
        self.negative = False

    # format NV-BDIZC
    def to_val(self):
        flags = [self.carry, self.zero, self.interrupt, self.decimal, self.brk, self.unused, self.overflow,
                 self.negative]
        return flags_to_val(flags)
