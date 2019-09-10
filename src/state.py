import src.register.register as reg
import src.register.statusregister as st_reg

class State:

    def __init__(self):
        self.a = reg.Register()
        self.x = reg.Register()
        self.y = reg.Register()
        self.pc = reg.Register()
        self.sp = reg.Register()
        self.status = st_reg.StatusRegister()

