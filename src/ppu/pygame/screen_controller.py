import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from .sprite import Sprite
from ..palette.palette import ColorMap, SpriteColorPalette, BackgroundColorPalette
from src.ppu.nametable.nametable import Nametable

size = (249, 230)

class ScreenController:
    TITLE = "Emulador Nes, grupo 4"

    def __init__(self, memory, oam):
        pygame.init()
        (x, y) = size
        self.screen = pygame.display.set_mode((2 * x, 2 * y))
        pygame.display.set_caption(ScreenController.TITLE)
        self.memory = memory
        self.oam = oam
        self.pixels = [ [0 for _ in range(264)] for _ in range(264) ]

    def init_info(self):
        self.sprite_palette = SpriteColorPalette(self.memory)
        self.background_palette = BackgroundColorPalette(self.memory)

    def set_sprites(self, sprites):
        self.sprites = sprites

    def get_reference_palette(self, is_background):
        if is_background:
            return self.background_palette

        return self.sprite_palette

    def draw_pixel(self, x, y, color):
        if (self.pixels[x][y] == color):
            return

        self.pixels[x][y] = color
        y -= 9
        x *= 2
        y *= 2
        pixel = pygame.Surface((2, 2))
        pixel.fill(color)
        self.screen.blit(pixel, (x, y))

    def get_sprite_data(self, number, is_background):
        if is_background:
            number += 0x100

        return self.sprites[number]

    def get_screen_pos(self, x, y, sprite):
        (base_x, base_y) = sprite.get_screen_position()

        if sprite.is_flipped_horintally():
            x = 7 - x

        if sprite.is_flipped_vertically():
            y = 7 - y

        return (base_x + x, base_y + y)

    def draw_sprite(self, sprite, is_background=False):
        if sprite.is_low_priority():
            return

        data = self.get_sprite_data(sprite.identifier, is_background)
        palette = self.get_reference_palette(is_background).get_palette(sprite.get_palette())
        for x in range(8):
            for y in range(8):
                pixel = data[y][x]
                if pixel or is_background:
                    color = ColorMap.get_color_rgb_reference(palette[pixel])
                    (base_x, base_y) = self.get_screen_pos(x, y, sprite)
                    self.draw_pixel(base_x, base_y, color)

    def draw(self):
        for pos in range(256):
            palette = 3
            sprite = Sprite(pos, ((pos % 16) * 8), ((pos // 16) * 8) + 9, 0b00000000 | palette)
            self.draw_sprite(sprite, False)

        for pos in range(256):
            palette = 3
            sprite = Sprite(pos, 0x80 + ((pos % 16) * 8), ((pos // 16) * 8) + 9, 0b00000000 | palette)
            self.draw_sprite(sprite, True)

    def draw_sprites(self, ptable_start):
        initial_addr = len(self.oam)

        for i in range(64):
            base_addr = initial_addr - ((i + 1) * 4)

            y = self.oam[base_addr + 0]
            x = self.oam[base_addr + 3]
            tile = self.oam[base_addr + 1]
            attributes = self.oam[base_addr + 2]

            self.draw_sprite(Sprite(tile, x, y, attributes), False)

    def display(self):
        pygame.display.flip()

    def decode_attribute_table(self, idx, entry):
        bottomright, bottomleft, topright, topleft = Nametable.get_bits(entry)

        x = (idx % 32) % 4
        y = (idx // 32) % 4

        if x // 2 and y // 2:
            return bottomright
        elif x // 2 and not y // 2:
            return topright
        elif not x // 2 and not y // 2:
            return topleft
        else:
            return bottomleft

    def draw_background(self, nametable_start, atable_start, ptable_start):

        nt_addr = nametable_start
        at_addr = atable_start
        pt_addr = ptable_start

        for idx in range(0x03C0):
            i = idx % 32
            j = idx // 32
            nt_entry = self.memory[nt_addr + idx]

            # Fetch the corresponding attribute table entry from $23C0-$23FF
            att_x = i // 4
            att_y = idx // 128
            att_idx = att_x + att_y * 8
            at_entry = self.memory[at_addr + att_idx]

            # Get the quadrant bits
            attribute = self.decode_attribute_table(idx, at_entry)

            sprite = Sprite(nt_entry, i * 8, j * 8, 0x0 | attribute)
            self.draw_sprite(sprite, True)
