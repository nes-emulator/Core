import pygame
from .sprite import Sprite
from ..palette.palette import ColorMap, SpriteColorPalette, BackgroundColorPalette
from src.memory.cpu.memory import Memory
from src.cpu.cpu import CPU

size = (255, 240)

COLOR = {
    0: (255, 55, 28),
    1: (255, 255, 255),
    2: (128, 128, 128),
    3: (55, 128, 244)
}

class ScreenController:
    def __init__(self):
        pygame.init()
        (x, y) = size
        self.game = pygame.display.set_mode((2 * x, 2 * y))

        memory = Memory(CPU())
        for i in range(32):
            memory.set_content(0x3F00 + i, i + 16)

        self.sprite_palette = SpriteColorPalette(memory)
        self.background_palette = BackgroundColorPalette(memory)


    def set_sprites(self, sprites):
        self.sprites = sprites

    def get_pixel_color(self, x, y):
        return (x, y, 255)

    def draw_pixel(self, x, y, color):
        x *= 2
        y *= 2
        self.game.set_at((x, y), color)
        self.game.set_at((x, y + 1), color)
        self.game.set_at((x + 1, y), color)
        self.game.set_at((x + 1, y + 1), color)

    def get_sprite_data(self, number, is_background):
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

        if sprite.attributes & 0b01000000:
            x = 7 - x

        if sprite.attributes & 0b10000000:
            y = 7 - y

        return (base_x + x, base_y + y)

    def draw_sprite(self, sprite, is_background=False):
        data = self.get_sprite_data(sprite.identifier, is_background)
        palette = self.sprite_palette.get_palette(sprite.attributes & 0b00000011)
        for x in range(8):
            for y in range(8):
                pixel = data[y][x]
                color = ColorMap.get_color_rgb_reference(palette[pixel])
                (base_x, base_y) = self.get_screen_pos(x, y, sprite)
                self.draw_pixel(base_x, base_y, color)

    def draw(self):
        for pos in range(512):
            palette = 0
            sprite = Sprite(pos, ((pos % 16) * 8), ((pos // 16) * 8), 0b00000000 | palette)
            self.draw_sprite(sprite, False)

        pygame.display.flip()