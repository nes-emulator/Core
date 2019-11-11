

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

    def clear_bit(self, n):
        mask = 1 << n
        self.value = self.value ^ mask

    def change_bit(self, n, val):
        if (val):
            self.set_bit(n)
        else:
            self.clear_bit(n)

    # Uses a list of bits to change values starting from low_bit
    def change_bits(self, low_bit, bits):
        current_bit = low_bit

        for bit in bits:
            if (bit):
                self.set_bit(current_bit)
            else:
                self.clear_bit(current_bit)

            current_bit += 1

    # Returns a list of n bits starting with low_bit
    def get_bits(self, low_bit, n):
        current_bit = low_bit
        bits = []

        for i in range(0, n):
            bits.append(self.get_bit(current_bit))
            current_bit += 1

        return bits

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
