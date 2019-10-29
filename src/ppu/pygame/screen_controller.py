import pygame
from .sprite import Sprite
from ..palette.palette import ColorMap, SpriteColorPalette, BackgroundColorPalette
from src.ppu.nametable.nametable import Nametable

size = (249, 230)

class ScreenController:
    def __init__(self, memory):
        pygame.init()
        (x, y) = size
        self.game = pygame.display.set_mode((2 * x, 2 * y))
        self.memory = memory

    def init_info(self):
        init_nametable(self.memory)
        self.sprite_palette = SpriteColorPalette(self.memory)
        self.background_palette = BackgroundColorPalette(self.memory)

    def set_sprites(self, sprites):
        self.sprites = sprites

    def get_reference_palette(self, is_background):
        if is_background:
            return self.background_palette

        return self.sprite_palette

    def draw_pixel(self, x, y, color):
        y -= 9

        x *= 2
        y *= 2
        self.game.set_at((x, y), color)
        self.game.set_at((x, y + 1), color)
        self.game.set_at((x + 1, y), color)
        self.game.set_at((x + 1, y + 1), color)

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

        pygame.display.flip()

    def draw_sprites(self):
        init_sprites(self.memory)
        initial_addr = 0x0200

        for i in range(64):
            base_addr = (initial_addr + 0x0100) - ((i + 1) * 4)

            y = self.memory[base_addr + 0]
            x = self.memory[base_addr + 3]
            tile = self.memory[base_addr + 1]
            attributes = self.memory[base_addr + 2]

            self.draw_sprite(Sprite(tile, x, y, attributes), False)

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

    def draw_background(self):
        start_nametable = 0x2000
        start_pattern_addr = 0

        nt_addr = start_nametable
        at_addr = 0x23C0
        pt_addr = 0x0000

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

        pygame.display.flip()


# TODO REMOVE THIS TESTS METHODS LATER
def init_nametable(memory):
    for i in range(0x20):
        memory[0x3F00 + i] = i

    for index in range(0x03BF + 1):
        memory[0x2000 + index] = 0x43

    for j in range(0x2400 - 0x23C0):
        value = (j % 4)
        memory[0x23C0 + j] = 0b0 | value

def write_sprite(memory, pos, tile, x, y, attributes):
    base_addr = 0x0200
    memory[base_addr + pos * 4 + 0] = y
    memory[base_addr + pos * 4 + 3] = x
    memory[base_addr + pos * 4 + 1] = tile
    memory[base_addr + pos * 4 + 2] = attributes

def init_sprites(memory):
    write_sprite(memory, 0, 0x10, 0x01, 0x01, 0b00000011) # first line invisible
    write_sprite(memory, 1, 0x00, 0x80, 0x80, 0b00100011)
    write_sprite(memory, 2, 0x45, 0x0A, 0xC7, 0b00000010)
    write_sprite(memory, 3, 0x99, 0xD8, 0x0C, 0b00000001)
    write_sprite(memory, 4, 0x99, 0x1A, 0xA7, 0b00000001)
    write_sprite(memory, 5, 0x00, 0x0A, 0xEF, 0b00000011) # invisible y
    write_sprite(memory, 6, 0x00, 0xF9, 0x29, 0b00000011) # invisible x
