class Nametable:

    def __init__(self):
        pass

    @staticmethod
    # each byte controls the palette of a 32x32 pixel area
    def get_bits(byte):
        # each byte is divided into four 2-bit areas
        topleft = byte & 0b00000011
        topright = byte & 0b00001100
        bottomleft = byte & 0b00110000
        bottomright = byte & 0b11000000

        return bottomright >> 6, bottomleft >> 4, topright >> 2, topleft
