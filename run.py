#!/usr/bin/env python

import atexit
import os
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from rgbmatrix import Adafruit_RGBmatrix

width          = 128  # Matrix size (pixels) -- change for different matrix
height         = 32  # types (incl. tiling).  Other code may need tweaks.
matrix         = Adafruit_RGBmatrix(32, 4) # rows, chain length
fps            = 20  # Scrolling speed (ish)

font           = ImageFont.load(os.path.dirname(os.path.realpath(__file__))
                   + '/helvR08.pil')
fontYoffset    = -2  # Scoot up a couple lines so descenders aren't croppe

# Main application -----------------------------------------------------------

# Drawing takes place in offscreen buffer to prevent flicker
image       = Image.new('RGB', (width, height))
draw        = ImageDraw.Draw(image)
currentTime = 0.0
prevTime    = 0.0

# Clear matrix on exit.  Otherwise it's annoying if you need to break and
# fiddle with some code while LEDs are blinding you.
def clearOnExit():
	matrix.Clear()

atexit.register(clearOnExit)

# Initialization done; loop forever ------------------------------------------
while True:

	# Clear background
	draw.rectangle((0, 0, width, height), fill=(0, 0, 0))



	# Try to keep timing uniform-ish; rather than sleeping a fixed time,
	# interval since last frame is calculated, the gap time between this
	# and desired frames/sec determines sleep time...occasionally if busy
	# (e.g. polling server) there'll be no sleep at all.
	currentTime = time.time()
	timeDelta   = (1.0 / fps) - (currentTime - prevTime)
	if(timeDelta > 0.0):
		time.sleep(timeDelta)
	prevTime = currentTime

	# Offscreen buffer is copied to screen
	matrix.SetImage(image.im.id, 0, 0)