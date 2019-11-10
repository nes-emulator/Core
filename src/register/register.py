

class Register:
    value = int('00000000', 2)

    def __init__(self, value=value):
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_bit(self, n):
        mask = 1 << n

        if (self.value & mask):
            return 1
        else:
            return 0

    def set_bit(self, n):
        mask = 1 << n
        self.value = self.value | mask

    def inc(self):
        self.value += 1

    def shift_left(self, amount, carry):
        self.value = self.value << amount
        if (carry):
            self.value += 1

    # works only for 8-bit registers
    def shift_right(self, amount, carry):
        self.value = self.value >> amount

        if (carry):
            self.value = self.value | 0b10000000
