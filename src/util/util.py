from math import log2
from math import ceil


def make_16b_binary(highByte, lowByte):
    return (highByte << 8) + lowByte


# return the result of x+y and carry in binary ;  with length = maxlen
def add_binary(x, y, maxlen):
    strx = bin(x)
    stry = bin(y)
    strx = strx.replace("0b", "")
    stry = stry.replace("0b", "")
    bitsx = [int(x) for x in strx]
    bitsy = [int(y) for y in stry]
    bitsx.reverse()
    bitsy.reverse()
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
