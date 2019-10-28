from src.ppu.nametable.nametable import Nametable
from src.util.util import extract_8_bits
from src.ppu.pygame.screen_controller import ScreenController


# this method will be called passing shared memory
def ppu_main(chr_rom, regs, memory, oam):  # , ctrl1, ctrl2)
    driver = Driver(chr_rom, regs, memory, oam)  # , ctrl1, ctrl2)
    driver.main()

def read_sprite_row(channel_a, channel_b):
    bits_a = extract_8_bits(channel_a)
    bits_b = extract_8_bits(channel_b)
    return [sum(e) for e in zip(bits_a, map(lambda x: x*2, bits_b))]

def get_sprites(chr_rom):
    idx = 0
    sprites = []
    for _ in range(512):
        sprite = []
        channel_a = chr_rom[idx : idx + 8]
        channel_b = chr_rom[idx + 8 : idx + 16]
        for i in range(8):
            sprite.append(read_sprite_row(channel_a[i], channel_b[i]))

        idx += 16
        sprites.append(sprite)

    return sprites


##### PPU MAIN DRIVER
class Driver:
    # DATA FROM REGISTERS

    # attribute_addr = {0x2000:0x23C0, 0x2400:0x27C0, 0x2800:0x2BC0, 0x2C00:0x2FC0}
    attribute_addr = {0: 0x23C0, 1: 0x27C0, 2: 0x2BC0, 3: 0x2FC0}
    background_pattern_addr = {0: 0x0, 1: 0x1000}

    # VRAM address increment per CPU read/write of PPUDATA

    def __init__(self, chr_rom, regs, memory, oam):  # , ctrl1, ctrl2)
        self.oam = oam
        self.regs = regs
        self.memory = memory
        self.chr_rom = chr_rom

    def main(self):
        game = ScreenController(self.memory)
        game.set_sprites(get_sprites(self.chr_rom))

        while True:
            game.init_info()
            game.draw_background()
            pass
