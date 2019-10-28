from multiprocessing import Array
from src.util.util import flags_to_val
import os, sys

# ommiting pygame print
with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame

    # enable stdout
    sys.stdout = oldstdout


class Controllers:
    Right = 0
    Left = 1
    Down = 2
    Up = 3
    Start = 4
    Select = 5
    B = 6
    A = 7
    BTN_NUMBER = 8
    CTRL1_ADDR = 0x4016
    CTRL2_ADDR = 0x4017

    # i've copied these bindings from mednafen config
    ctrl1_keybinds = {pygame.K_KP2: B, pygame.K_KP3: A, pygame.K_KP_ENTER: Start, pygame.K_TAB: Select,
                      pygame.K_s: Down, pygame.K_w: Up, pygame.K_a: Left, pygame.K_d: Right
                      }
    # controller 2 is disabled, for now
    ctrl2_keybinds = {}
    ctrl1_btn_states = Array('B', (0,) * BTN_NUMBER, lock=False)
    ctrl2_btn_states = Array('B', (0,) * BTN_NUMBER, lock=False)

    # loads the button state to memory when 1 is stored in the ctrl addr
    @classmethod
    def btn_loader(cls, mem_write):
        def button_state_loader(memory, addr, val):
            mem_write(memory, addr, val)
            if val == 1:
                if addr == cls.CTRL1_ADDR:
                    btn_state_wrapper = list(cls.ctrl1_btn_states)
                    btn_state_wrapper.reverse()
                    memory.memory[cls.CTRL1_ADDR] = flags_to_val(btn_state_wrapper)
                elif addr == cls.CTRL2_ADDR:
                    btn_state_wrapper = list(cls.ctrl2_btn_states)
                    btn_state_wrapper.reverse()
                    memory.memory[cls.CTRL2_ADDR] = flags_to_val(btn_state_wrapper)

        return button_state_loader

    # after reading btn state, we reset every button to "unpressed"
    @classmethod
    def reset_buttons_after_read(cls, memory_access_func):
        def btn_resseter(memory, addr):
            mem_val = memory_access_func(memory, addr)
            if addr == cls.CTRL1_ADDR:
                memory.memory[cls.CTRL1_ADDR] = 0
            elif addr == cls.CTRL2_ADDR:
                memory.memory[cls.CTRL2_ADDR] = 0
            return mem_val

        return btn_resseter

    # place this in main loop
    @classmethod
    def button_press(cls):
        keys = pygame.key.get_pressed()
        for btn, index in cls.ctrl1_keybinds.items():
            if keys[btn]:
                cls.ctrl1_btn_states[index] = 1
        for btn, index in cls.ctrl2_keybinds.items():
            if keys[btn]:
                cls.ctrl2_btn_states[index] = 1
