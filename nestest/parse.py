f = open("nestest.log", "r")

for line in f:
    opcode = line[0:4]
    print("PC:" + str(int(opcode, 16)) + ' ' + line[48:74])

f.close()
