import pygame
import numpy
import scipy.signal
from array import array
from time import sleep

from pygame.mixer import Sound, get_init, pre_init
from .pulse import PulseChannel
from .triangle import TriangleChannel
from .control_registers import ApuControl

CPU_CLOCK = 1789773
pre_init(44100, -16, 2, 1024)

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

class TriangleNote(Sound):
    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_sample())
        self.set_volume(volume)

    def build_sample(self):
        print(self.frequency)
        # wave = scipy.signal.triang(500 + int(self.frequency)) #
        wave = scipy.signal.triang(130 + int(self.frequency)) #
        amplitude = 2 ** (15) - 1
        sample = wave * amplitude
        sample = numpy.resize(sample, 44100)
        return sample.astype(numpy.int16)


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
    def play_tri(regs):
        channel = TriangleChannel(regs[8], regs[10], regs[11]) ## skips $4009
        timer = (channel.get_timer_high() << 8) + channel.get_timer_low()

        if not timer:
            return

        frequency = CPU_CLOCK / (32 * (timer + 1))
        # print(frequency)
        TriangleNote(frequency).play(20)
        # regs[8] = 0
        # regs[10] = 0
        # regs[11] = 0

    @staticmethod
    def play(regs):

        control = ApuControl(regs[15], regs[17])

        # if control.get_triangle_lc_enable() == 1:
        APUPlayState.play_tri(regs)

        APUPlayState.play_pulse(regs, 0)
        APUPlayState.play_pulse(regs, 4)
