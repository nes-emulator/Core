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



def add_binary(x, y, maxlen):
    return (x + y) % (2 ** maxlen)


def apply_mask(number, mask):
    return number & mask


def apply_lower_byte_mask(number):
    return number & 0xFF


def apply_higher_byte_mask(number):
    return (number >> 8) & 0xFF
