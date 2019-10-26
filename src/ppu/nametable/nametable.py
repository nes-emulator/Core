class Nametable:

    def __init__(self):
        # TODO: alloc nametable 960 bytes here
        # self.memory = array(Memory.UNSIGNED_BYTE_TYPE, (0,) * Memory.MEMORY_LIMIT)
        self.attribute_table = array(Memory.UNSIGNED_BYTE_TYPE, (0,) * 64)
    @staticmethod

    # each byte controls the palette of a 32x32 pixel area
    def get_bits(byte):
        # each byte is divided into four 2-bit areas
        bottomright = byte && 0b00000011
        bottomleft = byte && 0b00001100
        topright = byte && 0b00110000
        topleft = byte && 0b11000000

        return bottomright, bottomleft, topright, topleft
