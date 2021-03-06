#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
import ConfigParser
import logging
import os
import pika
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from rgbmatrix import Adafruit_RGBmatrix

from util import AutoBrightness
from widgets import Clock

width = 128  # Matrix size (pixels) -- change for different matrix
height = 32  # types (incl. tiling).  Other code may need tweaks.
matrix = Adafruit_RGBmatrix(32, 4)  # rows, chain length
fps = 10  # Scrolling speed (ish)

logging.basicConfig(level=logging.DEBUG , format='%(asctime)s %(levelname)8s %(name)s: %(message)s')
log = logging.getLogger(__name__)

# Main application -----------------------------------------------------------

# Load Config
SvcConfig = ConfigParser.ConfigParser()
SvcConfig.read("/etc/puphaus.ini")

# Connect to RabbitMQ
rmqCred = pika.PlainCredentials(SvcConfig.get('RabbitMQ', 'Username'), SvcConfig.get('RabbitMQ', 'Password'))
rmqConn = pika.BlockingConnection(pika.ConnectionParameters(host=SvcConfig.get('RabbitMQ', 'Host'),
                                                            port=SvcConfig.getint('RabbitMQ', 'Port'),
                                                            credentials=rmqCred,
                                                            ssl=True,
                                                            virtual_host='puphaus'))
rmqChan = rmqConn.channel()

# Drawing takes place in offscreen buffer to prevent flicker
image = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(image)
currentTime = 0.0
prevTime = 0.0

# Load Widgets
autoBright = AutoBrightness()
wdgtClock = Clock()


# Clear matrix on exit.  Otherwise it's annoying if you need to break and
# fiddle with some code while LEDs are blinding you.
def clearOnExit():
    matrix.Clear()


atexit.register(clearOnExit)

# Initialization done; loop forever ------------------------------------------
while True:
    brightness = autoBright.getBrightness()

    # Clear background
    draw.rectangle((0, 0, width, height), fill=(0, 0, 0))

    wdgtClock.draw(draw, 1, 2, brightness)

    # Try to keep timing uniform-ish; rather than sleeping a fixed time,
    # interval since last frame is calculated, the gap time between this
    # and desired frames/sec determines sleep time...occasionally if busy
    # (e.g. polling server) there'll be no sleep at all.
    currentTime = time.time()
    timeDelta = (1.0 / fps) - (currentTime - prevTime)
    if (timeDelta > 0.0):
        time.sleep(timeDelta)
    prevTime = currentTime

    # Offscreen buffer is copied to screen
    matrix.SetImage(image.im.id, 0, 0)
