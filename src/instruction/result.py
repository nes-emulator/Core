
class InstructionResult:
    a_register = None
    x_register = None
    y_register = None

    # TODO JUST AN IDEA, each one of these is to be a boolean
    zero_flag = None
    carry_flag = None

    def set_a_reg(self, value):
        self.a_register = value

    def set_x_reg(self, value):
        self.x_register = value

    def set_y_reg(self, value):
        self.y_register = value

    def set_zero_flag(self, flag):
        self.zero_flag = flag

    def set_carry_flag(self, flag):
        self.carry_flag = flag
