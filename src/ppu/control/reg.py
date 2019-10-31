from src.util.util import extract_flags, flags_to_val, flags_to_val_2

BASE_ADDR = 0x2000


# latch behavior
# Writing any value to any PPU port, even to the nominally read-only
# PPUSTATUS, will fill this latch.
# Reading any readable port (PPUSTATUS, OAMDATA, or PPUDATA) also fills the latch with the bits read

# NMI enable (V), PPU master/slave (P), sprite height (H), background tile select (B), sprite tile select (S), increment mode (I), nametable select (NN)
# Access: write
class PPUCTRL:
    BASE_ADDR = 0x2000

    def __init__(self, val):
        self.from_val(val)

    # VPHB SINN
    def from_val(self, val):
        flags = extract_flags(val, 8)
        self.nmi = flags[0]  # Generate an NMI at the start of the vertical blanking interval
        self.ppu_mas_sla = flags[1]  # (0: read backdrop from EXT pins; 1: output color on EXT pins
        self.ppu_sprite_height = flags[2]
        self.bg_tile = flags[3]
        self.sprite_tile = flags[4]
        self.increment_mode = flags[5]
        self.nametable_1 = flags[6]
        self.nametable_2 = flags[7]

    def extract_nametable_addr(self):
        return PPUCTRL.BASE_ADDR + flags_to_val([self.nametable_1, self.nametable_2]) * 0x400

    def extract_vram_increment(self):
        # (0: add 1, going across; 1: add 32, going down)
        return 32 if self.increment_mode else 1

    # Sprite pattern table address for 8x8 sprites
    # (0: $0000; 1: $1000; ignored in 8x16 mode)
    def extract_sprite_pattern_table_addr(self):
        return 0 if self.sprite_tile else 0x1000

    def extract_background_pattern_table(self):
        return 0 if self.bg_tile else 0x1000

    def to_val(self):
        flags = [self.nmi, self.ppu_mas_sla, self.ppu_sprite_height, self.bg_tile, self.sprite_tile,
                 self.increment_mode,
                 self.nametable_1, self.nametable_2]
        return flags_to_val(flags)


# This register controls the rendering of sprites and backgrounds, as well as colour effects.
# color emphasis (BGR), sprite enable (s), background enable (b), sprite left column enable (M), background left column enable (m), greyscale (G)
# Access: write
class PPUMASK:
    BASE_ADDR = 0x2001

    def __init__(self, val):
        self.from_val(val)

    # BGRs bMmG
    def from_val(self, val):
        flags = extract_flags(val, 8)
        self.cl_emph_B = flags[0]
        self.cl_emph_G = flags[1]
        self.cl_emph_R = flags[2]
        self.spr_enabled = flags[3]
        self.bg_enabled = flags[4]
        self.spr_left_col_enabled = flags[5]
        self.bg_left_col_enabled = flags[6]
        self.grey_scale = flags[7]

    def to_val(self):
        flags = [self.cl_emph_B, self.cl_emph_G, self.cl_emph_R, self.spr_enabled, self.bg_enabled,
                 self.spr_left_col_enabled,
                 self.bg_left_col_enabled, self.grey_scale]
        return flags_to_val_2(flags)


# It is often used for determining timing.
# To determine when the PPU has reached a given pixel of the screen,
# put an opaque (non-transparent) pixel of sprite 0 there

# vblank (V), sprite 0 hit (S), sprite overflow (O);
# read resets write pair for $2005/$2006
# Access: read
class PPUSTATUS:
    BASE_ADDR = 0x2002

    def __init__(self, val):
        self.from_val(val)

    def from_val(self, val):
        flags = extract_flags(val, 8)
        self.v = flags[0]
        self.s = flags[1]
        self.o = flags[2]

    def to_val(self):
        flags = [self.o, self.s, self.v]
        return flags_to_val(flags)


# OAM read / write address
# Write the address of OAM you want to access
# The value of OAMADDR when sprite evaluation starts at tick 65 of
# the visible scanlines will determine  where in OAM sprite evaluation starts
# For emulation purposes, it is probably best to completely ignore writes during rendering.
# OAMDMA is used instead of OAMADDR on most games
# Access: write
class OAMADDR:
    BASE_ADDR = 0x2003

    def __init__(self, val):
        self.read_write_addr = val

    def to_val(self):
        return self.read_write_addr


# OAM data read/write
# Access: read, write
# Write OAM data here. Writes will increment OAMADDR after the write
# changes to OAM should normally be made only during vblank
class OAMDATA:
    BASE_ADDR = 0x2004

    def __init__(self, val):
        self.data_read_write_addr = val

    def to_val(self):
        return self.data_read_write_addr


# fine scroll position (two writes: X scroll, Y scroll)
# Access: write twice
# write the 16-bit address of VRAM you want to access here
class PPUSCROLL:
    BASE_ADDR = 0x2005

    def __init__(self, val):
        self.fine_scroll_pos = val

    def to_val(self):
        return self.fine_scroll_pos


# PPU read / write address
# write the 16-bit address of VRAM you want to access here, upper byte first
# Access: write twice
# Valid addresses are $0000-$3FFF; higher addresses will be mirrored downtime
class PPUADDR:
    BASE_ADDR = 0x2006

    def __init__(self, val):
        self.ppu_read_write_addr = val

    def to_val(self):
        return self.ppu_read_write_addr


# PPU data read/write
# Access: read, write
# VRAM read/write data register. After access, the video memory address will increment by an amount determined by bit 2 of $2000.
# Since accessing this register increments the VRAM address, it should not be accessed outside vertical or forced blanking because it will cause graphical glitches

class PPUDATA:
    BASE_ADDR = 0x2007

    def __init__(self, val):
        self.ppu_data_read_write_addr = val

    def to_val(self):
        return self.ppu_data_read_write_addr


# This port is located on the CPU. Writing $XX will upload 256 bytes of data from CPU page $XX00-$XXFF to the internal PPU OAM.
# The DMA transfer will begin at the current OAM write address. It is common practice to initialize it to 0 with a write to OAMADDR before the DMA transfer
class OAMDMA:
    BASE_ADDR = 0x4014

    def __init__(self, val):
        self.oam_dma_high_addr = val

    def to_val(self):
        return self.oam_dma_high_addr
