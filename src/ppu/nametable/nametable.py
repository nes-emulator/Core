class Nametable:

    def __init__(self):
        # TODO: alloc nametable 960 bytes here
        # self.memory = array(Memory.UNSIGNED_BYTE_TYPE, (0,) * Memory.MEMORY_LIMIT)
        self.attribute_table = array(Memory.UNSIGNED_BYTE_TYPE, (0,) * 64)


    ### ATTRIBUTE TABLE
    # TODO: translate the hex addresses to access the linear array
    # TODO: there are four nametables $23C0, $27C0, $2BC0, or $2FC0

    # each byte controls the palette of a 32x32 pixel area
    # byte = get_byte()

    # each byte is divided into four 2-bit areas
    bottomright = byte && 0b00000011
    bottomleft = byte && 0b00001100
    topright = byte && 0b00110000
    topleft = byte && 0b11000000

    att_value = (bottomright << 6) | (bottomleft << 4) | (topright << 2) | (topleft)
