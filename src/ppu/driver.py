

##### PPU MAIN DRIVER

start_nametable = 0x2000

for i in range(33):
#     Fetch a nametable entry from $2000-$2FBF


#     Fetch the corresponding attribute table entry from $23C0-$2FFF and increment the current VRAM address within the same row.
#     Fetch the low-order byte of an 8x1 pixel sliver of pattern table from $0000-$0FF7 or $1000-$1FF7.
#     Fetch the high-order byte of this sliver from an address 8 bytes higher.
#     Turn the attribute data and the pattern table data into palette indices, and combine them with data from sprite data using priority.
