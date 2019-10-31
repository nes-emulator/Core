from src.ppu.nametable.nametable import Nametable
from src.util.util import extract_8_bits
from src.ppu.pygame.screen_controller import ScreenController
from src.ppu.control.reg import PPUCTRL, PPUSTATUS, PPUMASK
from src.ppu.pygame.controller import Controllers


# this method will be called passing shared memory

def ppu_main(chr_rom, regs, memory, oam, ctrl1, ctrl2):
    driver = Driver(chr_rom, regs, memory, oam, ctrl1, ctrl2)
    driver.main()


def read_sprite_row(channel_a, channel_b):
    bits_a = extract_8_bits(channel_a)
    bits_b = extract_8_bits(channel_b)
    return [sum(e) for e in zip(bits_a, map(lambda x: x * 2, bits_b))]


def get_sprites(chr_rom):
    idx = 0
    sprites = []
    for _ in range(512):
        sprite = []
        channel_a = chr_rom[idx: idx + 8]
        channel_b = chr_rom[idx + 8: idx + 16]
        for i in range(8):
            sprite.append(read_sprite_row(channel_a[i], channel_b[i]))

        idx += 16
        sprites.append(sprite)

    return sprites


##### PPU MAIN DRIVER
class Driver:

    def __init__(self, chr_rom, regs, memory, oam, ctrl1, ctrl2):
        self.oam = oam
        self.regs = regs
        self.memory = memory
        self.chr_rom = chr_rom
        self.attribute_table_addr = {0x2000: 0x23C0, 0x2400: 0x27C0, 0x2800: 0x2BC0, 0x2C00: 0x2FC0}

    def main(self):
        game = ScreenController(self.memory, self.oam)
        game.set_sprites(get_sprites(self.chr_rom))

        # FIRST RENDER, needs to display() twice

        # PPUCTRL
        ppuctrl = PPUCTRL(self.regs[0])
        base_nt_addr = ppuctrl.extract_nametable_addr()
        # TODO: vram_incr = ppuctrl.extract_vram_increment()
        sprite_pt_addr = ppuctrl.extract_sprite_pattern_table_addr()
        back_pt_addr = ppuctrl.extract_background_pattern_table()
        # TODO: sprite size

        # PPUMASK
        ppumask = PPUMASK(self.regs[1])
        show_sprites = ppumask.spr_enabled
        show_background = ppumask.bg_enabled

        # PPUSTATUS
        ppustatus = PPUSTATUS(self.regs[2])

        # render the game
        game.init_info()
        if (show_background):
            game.draw_background(base_nt_addr, self.attribute_table_addr[base_nt_addr], back_pt_addr)
        game.display()

        if (show_sprites):
            game.draw_sprites(sprite_pt_addr)
        game.display()

        while True:
            # parse control registers here

            # PPUCTRL
            ppuctrl = PPUCTRL(self.regs[0])
            if not ppuctrl.nmi:
                continue

            base_nt_addr = ppuctrl.extract_nametable_addr()
            # TODO: vram_incr = ppuctrl.extract_vram_increment()
            sprite_pt_addr = ppuctrl.extract_sprite_pattern_table_addr()
            back_pt_addr = ppuctrl.extract_background_pattern_table()
            # TODO: sprite size

            # PPUMASK
            ppumask = PPUMASK(self.regs[1])
            show_sprites = ppumask.spr_enabled
            show_background = ppumask.bg_enabled

            # PPUSTATUS
            ppustatus = PPUSTATUS(self.regs[2])

            # render the game
            game.init_info()
            if (show_background):
                game.draw_background(base_nt_addr, self.attribute_table_addr[base_nt_addr], back_pt_addr)
                # game.display()

            if (show_sprites):
                Controllers.button_press()
                game.draw_sprites(sprite_pt_addr)
                game.display()
