from multiprocessing import Array
import os, sys
import pygame


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

    ctrl1_bit_being_read = -1
    ctrl2_bit_being_read = -1

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
                    cls.ctrl1_bit_being_read = 0
                elif addr == cls.CTRL2_ADDR:
                    cls.ctrl2_bit_being_read = 0

        return button_state_loader

    # after reading btn state, we reset every button to "unpressed"
    @classmethod
    def read_button(cls, memory_access_func):
        def btn_resseter(memory, addr):
            mem_val = memory_access_func(memory, addr)
            if addr == cls.CTRL1_ADDR and cls.ctrl1_bit_being_read >= 0:
                mem_val = cls.ctrl1_btn_states[cls.ctrl1_bit_being_read]
                cls.ctrl1_btn_states[cls.ctrl1_bit_being_read] = 0
                cls.ctrl1_bit_being_read += 1
            elif addr == cls.CTRL2_ADDR and cls.ctrl2_bit_being_read >= 0:
                mem_val = cls.ctrl2_btn_states[cls.ctrl2_bit_being_read]
                cls.ctrl2_btn_states[cls.ctrl2_bit_being_read] = 0
                cls.ctrl2_bit_being_read += 1
            cls.reset_current_bit_if_limit(memory)
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

    @classmethod
    def reset_current_bit_if_limit(cls, mem):
        if cls.ctrl2_bit_being_read == cls.BTN_NUMBER:
            cls.ctrl2_bit_being_read = -1
            mem.memory[cls.CTRL2_ADDR] = 0
        if cls.ctrl1_bit_being_read == cls.BTN_NUMBER:
            cls.ctrl1_bit_being_read = -1
            mem.memory[cls.CTRL1_ADDR] = 0
