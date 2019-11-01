# PPUCTRL

## 1

If the PPU is currently in vertical blank, and the PPUSTATUS ($2002) vblank flag is still set (1), changing the NMI flag in bit 7 of $2000 from 0 to 1 will immediately generate an NMI. This can result in graphical errors (most likely a misplaced scroll) if the NMI routine is executed too late in the blanking period to finish on time. To avoid this problem it is prudent to read $2002 immediately before writing $2000 to clear the vblank flag.

# PPUMASK

## 1

Color control is not implemented.

# PPUSTATUS

## 1

Sprite 0 hit

## 2

Sprite Overflow

## 3

4 Lowest bits in the bus

# PPUADDR

## 1

Access to PPUSCROLL and PPUADDR during screen refresh produces interesting raster effects;
the starting position of each scanline can be set to any pixel position in nametable memory.
For more information, see PPU scrolling and tokumaru's sample code on the BBS.[9]

# PPUDATA

## 1

VRAM reading and writing shares the same internal address register that rendering uses.
So after loading data into video memory, the program should reload the scroll position afterwards
with PPUSCROLL writes in order to avoid wrong scrolling.

## 2

When reading while the VRAM address is in the range 0-$3EFF (i.e., before the palettes), the read will return the contents of an internal read buffer.
This internal buffer is updated only when reading PPUDATA, and so is preserved across frames. After the CPU reads and gets the contents of the internal buffer,
the PPU will immediately update the internal buffer with the byte at the current VRAM address.
Thus, after setting the VRAM address, one should first read this register and discard the result.
