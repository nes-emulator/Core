
class Sprite:
    x = None
    y = None
    identifier = None
    attributes = None

    def __init__(self, identifier, x, y, attributes):
        self.x = x
        self.y = y
        self.identifier = identifier
        self.attributes = attributes

    def get_screen_position(self):
        return (self.x, self.y)

    def is_flipped_horintally(self):
        return (self.attributes & 0b01000000) > 0

    def is_flipped_vertically(self):
        return (self.attributes & 0b10000000) > 0

    def get_palette(self):
        return self.attributes & 0b00000011

    def is_low_priority(self):
        return self.attributes & 0b00100000