class StatusRegister:
    def __init__(self, val=None):
        self.clear()
        if not val is None:
            str_val = bin(val)
            str_val = str_val.replace("0b", "")
            val = [bool(int(b)) for b in str_val]
            qtd_flags = len(val)
            if qtd_flags < 8:
                val = [False] * (8 - qtd_flags) + val
            # format NV-BDIZC/
            self.negative = val[0]
            self.overflow = val[1]
            self.unused = val[2]
            self.brk = val[3]
            self.decimal = val[4]
            self.interrupt = val[5]
            self.zero = val[6]
            self.carry = val[7]

    def clear(self):
        self.carry = False
        self.zero = False
        self.interrupt = True  # IRQ starts disabled
        self.decimal = False
        self.brk = True
        self.unused = True
        self.overflow = False
        self.negative = False

    # format NV-BDIZC
    def to_val(self):
        regs = [self.carry, self.zero, self.interrupt, self.decimal, self.brk, self.unused, self.overflow,
                self.negative]
        val = [i * (2 ** int(r)) for i, r in zip(regs, range(0, len(regs)))]
        return sum(val)
