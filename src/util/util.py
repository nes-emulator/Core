

def extract_bits(number):
    str_num = bin(number)
    str_num = str_num.replace("0b", "")
    bits = [int(x) for x in str_num]
    bits.reverse()
    return bits

def extract_8_bits(number):
    str_num = bin(number)
    str_num = str_num.replace("0b", "")
    bits = [int(x) for x in str_num]
    return [0] * (8 - len(bits)) + bits


def extract_flags(val, n_flags):
    flags = [bool(b) for b in extract_8_bits(val)]
    return [False] * (n_flags - len(flags)) + flags

# please dont call this
def flags_to_val(flags):
    flags = ([0] * (8 - len(flags))) + flags
    val = [i * (2 ** int(r)) for i, r in zip(flags, range(0, len(flags)))]
    return sum(val)

# Returns the decimal value of a bit sequence starting with the highest bit
def flags_to_val_2(flags):
    val = [i * (2 ** r) for i, r in zip(flags, range(len(flags) - 1, -1, -1))]
    return sum(val)

# Returns the decimal value of a bit sequence starting with the lowest bit
def flags_to_val_low(flags):
    val = [i * (2 ** int(r)) for i, r in zip(flags, range(0, len(flags)))]
    return sum(val)

def is_negative(number, n_digits):
    bits = extract_bits(number)
    if len(bits) < n_digits:
        return False
    return bits[n_digits - 1] == 1  # negative, last bit  == 1


def extract_2byteFrom16b(num):
    highbyte = apply_higher_byte_mask(num)
    lowebyte = apply_lower_byte_mask(num)
    return lowebyte, highbyte


def make_16b_binary(highByte, lowByte):
    return (highByte << 8) + lowByte


def add_binary_overflow(x, y, maxlen):
    return (x + y) % (2 ** maxlen)


def add_binary_overflow_255(x, y):
    return (x + y) & 0b11111111


def apply_mask(number, mask):
    return number & mask


def apply_lower_byte_mask(number):
    return number & 0xFF


def apply_higher_byte_mask(number):
    return (number >> 8) & 0xFF
