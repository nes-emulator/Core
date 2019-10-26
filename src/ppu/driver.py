from src.ppu.memory.ppu_mem import PPUMemory

##### PPU MAIN DRIVER
class Driver:

    # DATA FROM REGISTERS

    # attribute_addr = {0x2000:0x23C0, 0x2400:0x27C0, 0x2800:0x2BC0, 0x2C00:0x2FC0}
    attribute_addr = {0:0x23C0, 1:0x27C0, 2:0x2BC0, 3:0x2FC0}
    background_pattern_addr = {0:0x0, 1:0x1000}

    # VRAM address increment per CPU read/write of PPUDATA

    def __init__(self):
        self.memory = PPUMemory()

    @staticmethod
    def decode_attribute_table(x, y, entry):

        bottomright, bottomleft, topright, topleft = Nametable.get_bits(entry)

        if x % 2 and y % 2:
            return bottomright
        elif x % 2 and not y % 2:
            return bottomleft
        elif not x % 2 and not y % 2:
            return topleft
        else:
            return topright

    def main(self, regs, memory, oam):

        start_nametable = 0
        start_pattern_addr = 0

        nt_addr = start_nametable
        at_addr = attribute_addr[start_nametable]
        pt_addr = background_pattern_addr[start_pattern_addr]

        # TODO:
        for i in range(31):
            for j in range(33):

                # linear array -> 2d array
                idx = (i * 32 + j)
                # Fetch a nametable entry from $2000-$2FBF
                nt_entry = self.memory.get_content(nt_addr + idx)

                # Fetch the corresponding attribute table entry from $23C0-$2FFF
                att_x = idx % 32
                att_y = idx // 2
                att_idx = att_x * 8 + att_y
                at_entry = self.memory.get_content(at_addr + att_idx)

                # Get the quadrant bits
                attribute = decode_attribute_table(x, y, at_entry)

                # Fetch the low-order byte of an 8x1 pixel sliver of pattern table from $0000-$0FF7 or $1000-$1FF7.
                # Fetch the high-order byte of this sliver from an address 8 bytes higher.
                # lo_pt_entry = self.memory.get_content(pt_addr)
                # hi_pt_entry = self.memory.get_content(pt_addr+1)

                # Turn the attribute data and the pattern table data into palette indices

                # and combine them with data from sprite data using priority.
