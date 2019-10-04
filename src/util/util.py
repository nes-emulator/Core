from math import log2
from math import ceil


def extract_bits(number):
    str_num = bin(number)
    str_num = str_num.replace("0b", "")
    bits = [int(x) for x in str_num]
    bits.reverse()
    return bits


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


# return the result of x+y and carry in binary ;  with length = maxlen
def add_binary(x, y, maxlen):
    bitsx = extract_bits(x)
    bitsy = extract_bits(y)
    pos = 0;
    c = 0
    res = []
    for xb, yb in zip(bitsx, bitsy):
        if pos == maxlen:
            break
        pos += 1
        local_sum = c + xb + yb
        c = 1
        if local_sum == 3:
            res.append(1)
        elif local_sum == 2:
            res.append(0)
        else:  # 0 or 1
            c = 0
            res.append(local_sum)

    if pos < maxlen and max(len(bitsx), len(bitsy)) > pos:
        gt = bitsx[pos:] if len(bitsx) > len(bitsy) else bitsx[pos:]
        for b in gt:
            if pos > maxlen:
                break
            pos += 1
            local_sum = c + b
            if local_sum > 1:
                c = 1
                res.append(0)
            else:
                res.append(local_sum)
                c = 0

    return sum([bit * 2 ** (idx) for bit, idx in zip(res, range(0, len(res)))]), c

def add_binary_2(x, y):
    return (x + y) & 0b11111111


def apply_mask(number, mask):
    return number & mask


def apply_lower_byte_mask(number):
    return number & 0xFF


def apply_higher_byte_mask(number):
    return (number >> 8) & 0xFF
