from multiprocessing import Array
import os, sys
import pygame


class Controllers:
    Right = 7
    Left = 6
    Down = 5
    Up = 4
    Start = 3
    Select = 2
    B = 1
    A = 0
    BTN_NUMBER = 8
    CTRL1_ADDR = 0x4016
    CTRL2_ADDR = 0x4017
    ctrl1_bit_being_read = 0
    ctrl2_bit_being_read = 0

    # i've copied these bindings from mednafen config
    ctrl1_keybinds = {pygame.K_KP2: B, pygame.K_SPACE: A, pygame.K_KP_ENTER: Start, pygame.K_TAB: Select,
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
            if addr == cls.CTRL1_ADDR and val & 0x1 == 0x1:
                cls.ctrl1_bit_being_read = 0

        return button_state_loader

    @classmethod
    def read_button(cls, memory_access_func):
        def btn_resseter(memory, addr):
            mem_val = memory_access_func(memory, addr)
            if cls.ctrl1_bit_being_read > 7:
                return mem_val

            if addr == cls.CTRL1_ADDR:
                mem_val = cls.ctrl1_btn_states[cls.ctrl1_bit_being_read]
                cls.ctrl1_bit_being_read += 1
            elif addr == cls.CTRL2_ADDR:
                mem_val = cls.ctrl2_btn_states[cls.ctrl2_bit_being_read]
                cls.ctrl2_bit_being_read += 1
            return mem_val

        return btn_resseter

    # place this in main loop
    @classmethod
    def button_press(cls, ppu_running):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in cls.ctrl1_keybinds:
                    index = cls.ctrl1_keybinds[event.key]
                    cls.ctrl1_btn_states[index] = 1
                elif event.key in cls.ctrl2_keybinds:
                    index = cls.ctrl2_keybinds[event.key]
                    cls.ctrl2_btn_states[index] = 1
            elif event.type == pygame.KEYUP:
                if event.key in cls.ctrl1_keybinds:
                    index = cls.ctrl1_keybinds[event.key]
                    cls.ctrl1_btn_states[index] = 0
                elif event.key in cls.ctrl2_keybinds:
                    index = cls.ctrl2_keybinds[event.key]
                    cls.ctrl2_btn_states[index] = 0
            elif event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                ppu_running.value = 0  # disable cpu
                exit(0)
