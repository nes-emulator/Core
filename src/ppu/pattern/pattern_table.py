

class PatternTable:
    pattern = []

    def get_all_tiles(self, mem):
        initial_address = 0x0000
        while initial_address < 0x1000:
            self.get_tile(mem, initial_address)
            initial_address += 0x0010

    def get_tile(self, mem, address):
        initial = address & 0x11111100
        for i in range(8):
            left_plane = mem.retrieve_content(initial + i)
            right_plane = mem.retrieve_content(initial + i + 8)

            for j in range(8):
                mask = (1 << (7 - j))
                bit_left = 1 if left_plane & mask else 0
                bit_right = 1 if right_plane & mask else 0
                self.pattern.append(self.get_unified_planes_value(bit_right, bit_left))

    def get_unified_planes_value(self, a, b):
        return (a << 1) + b

    def bitfield(self, n):
        return [1 if digit=='1' else 0 for digit in bin(n)[2:]]