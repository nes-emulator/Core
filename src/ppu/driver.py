from src.ppu.nametable.nametable import Nametable
from src.util.util import extract_8_bits
from src.ppu.pygame.screen_controller import ScreenController
from src.ppu.control.reg import PPUCTRL, PPUSTATUS, PPUMASK
from src.ppu.pygame.controller import Controllers
from src.apu.play import APUPlayState
import pygame

# this method will be called passing shared memory

def ppu_main(chr_rom, regs, apu_regs, memory, oam, ppu_running):
    driver = Driver(chr_rom, regs, apu_regs, memory, oam, ppu_running)
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

    def __init__(self, chr_rom, regs, apu_regs, memory, oam, ppu_running):
        self.oam = oam
        self.regs = regs
        self.memory = memory
        self.chr_rom = chr_rom
        self.apu_regs = apu_regs
        self.attribute_table_addr = {0x2000: 0x23C0, 0x2400: 0x27C0, 0x2800: 0x2BC0, 0x2C00: 0x2FC0}
        self.ppu_running = ppu_running

    def main(self):
        game = ScreenController(self.memory, self.oam)
        game.set_sprites(get_sprites(self.chr_rom))

        while self.ppu_running:
            # window closed ?
            # parse controllers
            Controllers.button_press(self.ppu_running)

            # parse control registers here
            # PPUCTRL
            ppuctrl = PPUCTRL(self.regs[0])
            if not ppuctrl.nmi:
                continue

            base_nt_addr = ppuctrl.extract_nametable_addr()
            sprite_pt_addr = ppuctrl.extract_sprite_pattern_table_addr()
            back_pt_addr = ppuctrl.extract_background_pattern_table()
            # TODO: sprite size

            # PPUMASK
            ppumask = PPUMASK(self.regs[1])
            show_sprites = ppumask.spr_enabled
            show_background = ppumask.bg_enabled

            # render the game
            game.init_info()
            if (show_background):
                game.draw_background(base_nt_addr, self.attribute_table_addr[base_nt_addr], back_pt_addr)

            if (show_sprites):
                game.draw_sprites(sprite_pt_addr)

            game.display()
            APUPlayState.play(self.apu_regs)
            # disable NMI bit in PPUSTATUS
            # TODO: clear this based on timing
            # self.regs[2] = self.regs[2] & 0b01111111
