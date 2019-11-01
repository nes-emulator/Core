

# PPUADDR

## 1

Access to PPUSCROLL and PPUADDR during screen refresh produces interesting raster effects;
the starting position of each scanline can be set to any pixel position in nametable memory.
For more information, see PPU scrolling and tokumaru's sample code on the BBS.[9]

## 2

Is this readable? What happens if you try to?

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
