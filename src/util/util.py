from math import log2
from math import ceil


def make_16b_binary(highByte, lowByte):
    return highByte << 4 + lowByte


# return the result of x+y and carry in binary ;  with length = maxlen
def add_binary(x, y, maxlen):
    strx = bin(x)
    stry = bin(y)
    strx = strx.replace("0b", "")
    stry.replace("0b", "")
    bitsx = [int(x) for x in strx].__reversed__()
    bitsy = [int(y) for y in stry].__reversed__()
    pos = 0;
    c = 0
    res = []
    for xb, yb in zip(bitsx, bitsy):
        if pos == maxlen:
            break
        pos += 1
        sum = c + xb + yb
        c = 1
        if sum == 3:
            res.append(1)
        elif sum == 2:
            res.append(0)
        else:  # 0 or 1
            c = 0
            res.append(sum)

    if pos < maxlen and max(len(bitsx), len(bitsy)) > pos:
        gt = bitsx[pos:] if len(bitsx) > len(bitsy) else bitsx[pos:]
        for b in gt:
            if pos > maxlen:
                break
            pos += 1
            sum = c + b
            if sum > 1:
                c = 1
                res.append(0)
            else:
                res.append(sum)
                c = 0

    return sum([b ** (i * 2) for b, i in zip(res, range(0, len(res)))]), c
