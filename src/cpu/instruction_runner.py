from src.instruction.collection import InstructionCollection
from src.instruction.addressing import *
from .logger import Logger
from datetime import datetime

class Runner:
    PRG_ROM_START = 0
    LOGGER_ACTIVE = True
    CPU_FREQUENCY_HZ = 1789773

    @staticmethod
    def run(prg_rom, cpu, mem):
        cpu.state.pc.set_value(Runner.PRG_ROM_START)

        while cpu.state.pc.get_value() < len(prg_rom):
            # TODO regulate stall
            params = []
            ins = InstructionCollection.get_instruction(prg_rom[cpu.state.pc.get_value()])
            for _ in range(getattr(ins, 'parameter_length', 0)):
                cpu.state.pc.inc()
                params.append(prg_rom[cpu.state.pc.get_value()])

            cpu.state.pc.inc()
            # start_time = datetime.now()
            manipulated_mem_addr = ins.execute(memory=mem, cpu=cpu, params=params)
            if Runner.LOGGER_ACTIVE:
                Logger.log_reg_status(cpu.state)
                if not manipulated_mem_addr is None:
                    Logger.log_mem_manipulation(mem, manipulated_mem_addr)
                Logger.next_log_line()

            # print ("TIME TO LOG STUFF %s" % str((datetime.now() - start_time).total_seconds()))
            # interval = datetime.now() - start_time
            # cpu_period = (1 / Runner.CPU_FREQUENCY_HZ) * ins.get_cycles()
            # delay = cpu_period - interval.total_seconds()
            # print ("EMULATOR TIME INTERVAL: %s / CPU PERIOD: %s / DIFF: %s " % (str(interval.total_seconds()), str(cpu_period), str(delay)))

    @classmethod
    def activate_log(cls):
        Runner.LOGGER_ACTIVE = True

    @classmethod
    def deactivate_log(cls):
        Runner.LOGGER_ACTIVE = False
