import pygame
from array import array
from time import sleep
from pygame.mixer import Sound, get_init, pre_init
from .pulse import PulseChannel

CPU_CLOCK = 1789773
pre_init(44100, -16, 1, 1024)

class PulseNote(Sound):
    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples

class APUPlayState:

    @staticmethod
    def play_pulse(regs, start_index):
        pulse = PulseChannel(regs[start_index], regs[start_index + 1], regs[start_index + 2], regs[start_index + 3])
        timer = (pulse.get_timer_high() << 8) + pulse.get_timer_low()
        if timer > 7:
            volume = pulse.get_volume() / 15
            frequency = CPU_CLOCK / (16 * (timer + 1))
            PulseNote(frequency, volume).play(timer)
            regs[start_index] = 0
            regs[start_index + 2] = 0
            regs[start_index + 3] = 0

    @staticmethod
    def play(regs):
        APUPlayState.play_pulse(regs, 0)
        APUPlayState.play_pulse(regs, 4)