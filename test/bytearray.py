import os
import struct
binFolder = "/home/work/cbas/bin"
file = os.path.join( binFolder, "test.bin" )

lines = [
    bytearray(b"hallo"),
    bytearray(b"welt")
]
with open(file, 'wb') as f:
    for line in lines:
        #b = bytes(line)
        #for b in line:
        #b1 = (b).to_bytes(1, byteorder='big', signed=False)
        b1 = struct.pack("{}b".format(len(line)), *line)
        f.write(b1)