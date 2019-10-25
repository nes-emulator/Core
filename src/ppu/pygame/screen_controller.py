import pygame
from .sprite import Sprite
from ..palette.palette import ColorMap, SpriteColorPalette, BackgroundColorPalette
from src.memory.memory import Memory
from src.cpu.cpu import CPU

size = (249, 230)

class ScreenController:
    def __init__(self):
        pygame.init()
        (x, y) = size
        self.game = pygame.display.set_mode((2 * x, 2 * y))

        self.memory = Memory(CPU())
        for i in range(32):
            self.memory.set_content(0x3F00 + i, i)

        self.sprite_palette = SpriteColorPalette(self.memory)
        self.background_palette = BackgroundColorPalette(self.memory)


    def set_sprites(self, sprites):
        self.sprites = sprites

    def get_pixel_color(self, x, y):
        return (x, y, 255)

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

    def update(self):
        (max_x, max_y) = size
        for x in range(max_x):
            for y in range(max_y):
                color = self.get_pixel_color(x, y)
                self.draw_pixel(x, y, color)

        pygame.display.flip()

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
        palette = self.sprite_palette.get_palette(sprite.get_palette())
        for x in range(8):
            for y in range(8):
                pixel = data[y][x]
                color = ColorMap.get_color_rgb_reference(palette[pixel])
                (base_x, base_y) = self.get_screen_pos(x, y, sprite)
                self.draw_pixel(base_x, base_y, color)

    def draw(self):
        for pos in range(512):
            palette = 3
            sprite = Sprite(pos, ((pos % 16) * 8), ((pos // 16) * 8), 0b00000000 | palette)
            self.draw_sprite(sprite, False)

        pygame.display.flip()

    def draw_sprites(self):
        init_sprites(self.memory)

        for i in range(64):
            base_addr = 0x0300 - ((i + 1) * 4)

            y = self.memory.retrieve_content(base_addr + 0)
            x = self.memory.retrieve_content(base_addr + 3)
            tile = self.memory.retrieve_content(base_addr + 1)
            attributes = self.memory.retrieve_content(base_addr + 2)

            self.draw_sprite(Sprite(tile, x, y, attributes), False)

        pygame.display.flip()

def write_sprite(memory, pos, tile, x, y, attributes):
    base_addr = 0x0200
    memory.set_content(base_addr + pos * 4 + 0, y)
    memory.set_content(base_addr + pos * 4 + 3, x)
    memory.set_content(base_addr + pos * 4 + 1, tile)
    memory.set_content(base_addr + pos * 4 + 2, attributes)

def init_sprites(memory):
    write_sprite(memory, 0, 0x10, 0x01, 0x01, 0b00000011) # first line invisible
    write_sprite(memory, 1, 0x00, 0x80, 0x80, 0b00100011)
    write_sprite(memory, 2, 0x45, 0x0A, 0xC7, 0b00000010)
    write_sprite(memory, 3, 0x99, 0xD8, 0x0C, 0b00000001)
    write_sprite(memory, 4, 0x99, 0x1A, 0xA7, 0b00000001)
    write_sprite(memory, 5, 0x00, 0x0A, 0xEF, 0b00000011) # invisible y
    write_sprite(memory, 6, 0x00, 0xF9, 0x29, 0b00000011) # invisible x
