# ------------------------------------- #
# Transform a json palette to an image. #
# Used by eww.                          #
# ------------------------------------- #

import sys
import json
from PIL import Image, ImageDraw

file = sys.argv[1]
save = sys.argv[2]

PALETTE_KEYS = ['com_fg', 'fg', 'com_acc', 'accent', 'com_bg', 'bg']

data = json.load(open(file, 'r'))

img = Image.new("RGB", (100, 300), 'red')
draw = ImageDraw.Draw(img)

for i, key in enumerate(PALETTE_KEYS):
    shape = [0, i * 50, 100, i * 50 + 50]
    draw.rectangle(shape, fill = data[key])

draw = ImageDraw.Draw(img)
img.save(save)