import pygame

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

    def get_sprite_data(self, number):
        return self.sprites[number]

    def update(self):
        (max_x, max_y) = size
        for x in range(max_x):
            for y in range(max_y):
                color = self.get_pixel_color(x, y)
                self.draw_pixel(x, y, color)

        pygame.display.flip()

    def draw(self):
        for pos in range(512):
            data = self.get_sprite_data(pos)
            for x in range(8):
                for y in range(8):
                    pixel = data[x][y]
                    base_x = y + ((pos % 32) * 8)
                    base_y = x + ((pos // 32) * 8)
                    self.draw_pixel(base_x, base_y, COLOR[pixel])

        pygame.display.flip()