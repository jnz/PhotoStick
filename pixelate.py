#!/usr/bin/python3

import sys
from PIL import Image

if len(sys.argv) < 2:
    print("%s imagefile" % sys.argv[0])
    sys.exit(1)

in_name = sys.argv[1]
pos_dot = in_name.rfind('.')
if pos_dot != -1:
    out_name = in_name[0:pos_dot]
else:
    out_name = in_name
out_name = out_name[0:7] + ".pix"

try:
    im = Image.open(in_name)
    if im.width >= 2**16:
        print("Image too wide!")
        sys.exit(1)

    if im.height != 288:
        print("Height is not 288, resizing...")
        im = im.resize((im.width, 288))

    im = im.convert('RGB')
    with open(out_name, "wb") as pix_file:
        pix_file.write(im.width.to_bytes(2, byteorder='little'))
        pix_file.write(b"\x00" * 1022)
        for col in range(0, im.width):
            for row in range(0, 288):
                r, g, b = im.getpixel((col, 288 - row - 1)) # flip
                pix_file.write(r.to_bytes(1, byteorder='little'))
                pix_file.write(g.to_bytes(1, byteorder='little'))
                pix_file.write(b.to_bytes(1, byteorder='little'))
            pix_file.write(b"\x00" * (1024 - 288 * 3))
except IOError as e:
    print(e)
    sys.exit(1)