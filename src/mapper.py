from enum import IntEnum, unique


@unique
class MapperType(IntEnum):
    NROM = 0x0


class Mapper():
    def __init__(self, _mapper_type, _cartridge):
        self.mapper_type = _mapper_type

    def get_mapper_type(self):
        return self.mapper_type


class NromMapper(Mapper):
    ###############################################################################
    # NROM (https://wiki.nesdev.com/w/index.php/NROM)
    ###############################################################################
    # iNES mappers: 000
    # CHR capacity: 8KB
    # PRG ROM capacity: 16KB or 32KB
    # PRG RAM capacity: 2KB or 4KB in Family Basic only
    ###############################################################################
    # Banks:
    # -----------------------------------------------------------------------------
    # CPU $6000-$7FFF: Family Basic only: PRG RAM
    # CPU $8000-$BFFF: First 16 KB of ROM
    # CPU $C000-$FFFF: Last 16 KB of ROM (NROM-256) or mirror of $8000-$BFFF (NROM-128)
    ###############################################################################

    def __init__(self, _cartridge):
        Mapper.__init__(self, MapperType.NROM, _cartridge)
