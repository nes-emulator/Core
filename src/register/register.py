

class Register:
    value = int('00000000', 2)

    def __init__(self, value=value):
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def shift_left(self, carry):
        pass

    def shift_right(self, carry):
        pass