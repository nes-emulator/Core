class Cartridge():
    ###############################################################################
    # NES file content
    ###############################################################################
    # Extracted from Marat Fayzullin .NES creator site -
    #               http://fms.komkon.org/EMUL8/NES.html
    ###############################################################################
    # Byte     Contents
    # -----------------------------------------------------------------------------
    # 0-3      String "NES^Z" used to recognize .NES files.
    # 4        Number of 16kB ROM banks.
    # 5        Number of 8kB VROM banks.
    # 6        bit 0     1 for vertical mirroring, 0 for horizontal mirroring.
    #          bit 1     1 for battery-backed RAM at $6000-$7FFF.
    #          bit 2     1 for a 512-byte trainer at $7000-$71FF.
    #          bit 3     1 for a four-screen VRAM layout.
    #          bit 4-7   Four lower bits of ROM Mapper Type.
    # 7        bit 0     1 for VS-System roms.
    #          bit 1-3   Reserved, must be zeroes!
    #          bit 4-7   Four higher bits of ROM Mapper Type.
    # 8        Number of 8kB RAM banks. For compatibility with the previous
    #          versions of the .NES format, assume 1x8kB RAM page when this
    #          byte is zero.
    # 9        bit 0     1 for PAL roms, otherwise assume NTSC.
    #          bit 1-7   Reserved, must be zeroes!
    # 10-15    Reserved, must be zeroes!
    # 16-...   ROM banks, in ascending order. If a trainer is present, its
    #          512 bytes precede the ROM bank contents.
    # ...- EOF  VROM banks, in ascending order.
    ###############################################################################

    def __init__(self, _cartridge_path):

        self.cartridge_path = _cartridge_path

        self.prg_rom = None
        self.chr_rom = None
        self.rom_banks = None
        self.vrom_banks = None
        self.mapper_type = 0
        self.extended_ram_exists = False
        self.name_table_mirroring = None

        self.load_cartridge()

    def get_mapper_type(self):
        return self.mapper_type

    def load_cartridge(self):
        with open(self.cartridge_path, 'rb') as cartridge_file:
            # Read the 0x10 bytes of Header
            header = cartridge_file.read(0x10)

            if (header[0:4] != b'NES\x1A'):
                raise ValueError("\nIt is not a valid NES header. Expected first four header values:"
                                            " b'NES\\x1A'. Found first four values: %s" % header[0:4])

            # Read the total number of 16kB ROM banks
            self.rom_banks = header[4]

            print("Number of 16kB PRG-ROM banks: %s" % str(self.rom_banks))

            # Read the total number of 8kB VROM banks
            self.vrom_banks = header[5]

            print("Number of 16kB PRG-ROM banks: %s" % str(self.vrom_banks))

            # 0xB = 1011b (the zero is due to Trainer not being supported)
            self.name_table_mirroring = header[6] & 0xB

            print("Name table mirroring: %s" % str(self.name_table_mirroring))

            # Getting the four lower bits of ROM Mapper Type (alfa = header[6] >> 4)
            # Verifies which one of the four bits are set (alfa = alfa | 0xf)
            # Getting the four higher bits of ROM Mapper Type (beta = header[7] & 0xf0)
            # Joining the higher with the lower bits (self.mapper_type = alfa | beta)
            self.mapper_type = ((header[6] >> 4) & 0xf) | (header[7] & 0xf0)

            print("Mapper number: %d" % int(self.mapper_type))

            # If there is a battery in the cartridge,
            # then there is an extended cpu ram
            if header[6] & 0x2: # 0x2 = 10b
                self.extended_ram_exists = True
                print("Cartridge uses extended RAM")
            else:
                print("Cartridge does not use extended RAM")

            if (header[6] & 0x4):
                raise ValueError("Cartridge uses trainer, but this functionality is not supported.")

            # Reads all 16kB PRG-ROM banks
            self.prg_rom = cartridge_file.read(0x4000 * self.rom_banks)
            if not self.prg_rom:
                raise ValueError("The number of PRG-ROM banks is invalid. Should be greater than 0.")

            # Reads all 8kB CHR-ROM banks
            if self.vrom_banks:
                self.chr_rom = cartridge_file.read(0x2000 * self.rom_banks)

                print("Cartridge uses CHR-ROM")
            else:
                print("Cartridge uses CHR-RAM")

    def get_prg_rom(self):
        return self.prg_rom

    def print_prg_as_binary(self):
        for instr in self.prg_rom:
            print(format(int(instr), "08b"))
