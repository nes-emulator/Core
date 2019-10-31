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
    ctrl1_bit_being_read = 0
    ctrl2_bit_being_read = 0

    # i've copied these bindings from mednafen config
    ctrl1_keybinds = {pygame.K_KP2: B, pygame.K_KP3: A, pygame.K_KP_ENTER: Start, pygame.K_TAB: Select,
                      pygame.K_s: Down, pygame.K_w: Up, pygame.K_a: Left, pygame.K_d: Right
                      }
    # controller 2 is disabled, for now
    ctrl2_keybinds = {}
    ctrl1_btn_states = Array('B', (0,) * BTN_NUMBER, lock=False)
    ctrl2_btn_states = Array('B', (0,) * BTN_NUMBER, lock=False)

    @classmethod
    def read_button(cls, memory_access_func):
        def btn_resseter(memory, addr):
            mem_val = memory_access_func(memory, addr)
            if addr == cls.CTRL1_ADDR:
                mem_val = cls.ctrl1_btn_states[cls.ctrl1_bit_being_read]
                cls.ctrl1_btn_states[cls.ctrl1_bit_being_read] = 0
                cls.ctrl1_bit_being_read += 1
                cls.ctrl1_bit_being_read %= cls.BTN_NUMBER
            elif addr == cls.CTRL2_ADDR:
                mem_val = cls.ctrl2_btn_states[cls.ctrl2_bit_being_read]
                cls.ctrl2_btn_states[cls.ctrl2_bit_being_read] = 0
                cls.ctrl2_bit_being_read += 1
                cls.ctrl2_bit_being_read %= cls.BTN_NUMBER
            return mem_val

        return btn_resseter

    # place this in main loop
    @classmethod
    def button_press(cls):

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.KEYDOWN:
                if cls.ctrl1_keybinds[event.key]:
                    index = cls.ctrl1_keybins[event.key]
                    cls.ctrl1_btn_states[index] = 1

                if cls.ctrl2_keybinds[event.key]:
                    index = cls.ctrl2_keybins[event.key]
                    cls.ctrl2_btn_states[index] = 1
