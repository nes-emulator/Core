from src.ppu.control.command_wrapper import CommandWrapper


class PPURegCallback:

    @staticmethod
    def ctrl_write(memory, cmd_wrapper) -> CommandWrapper:
        pass

    @staticmethod
    def mask_write(memory, cmd_wrapper) -> CommandWrapper:
        pass

    @staticmethod
    def status_read(memory, cmd_wrapper) -> CommandWrapper:
        pass

    @staticmethod
    def oam_addr_write(memory, cmd_wrapper) -> CommandWrapper:
        pass

    @staticmethod
    def oam_data_read(memory, cmd_wrapper) -> CommandWrapper:
        pass

    @staticmethod
    def oam_data_write(memory, cmd_wrapper) -> CommandWrapper:
        pass

    @staticmethod  # write twice
    def scroll_write(memory, cmd_wrapper) -> CommandWrapper:
        pass

    @staticmethod  # write twice
    def ppu_addr_write(memory, cmd_wrapper) -> CommandWrapper:
        pass

    @staticmethod
    def ppu_addr_read(memory, cmd_wrapper) -> CommandWrapper:
        pass

    @staticmethod
    def ppu_data_read(memory, cmd_wrapper) -> CommandWrapper:
        pass

    @staticmethod
    def ppu_data_write(memory, cmd_wrapper) -> CommandWrapper:
        pass


    @staticmethod
    def oam_dma_write(memory, cmd_wrapper) -> CommandWrapper:
        pass
