#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os

from PIL import ImageFont

from util import scaleColor

#defaultFont   = ImageFont.load(os.path.dirname(os.path.realpath(__file__)) + '/helvR08.pil')
fontPixelMillennium = ImageFont.truetype("fonts/PixelMillennium.ttf", 8)
class Clock:
    def __init__(self):
        self.colorDay = (255, 255, 128)
        self.colorNight = (128, 128, 255)
        self.colorToday = (0, 255, 0)
        self.colorDate = (255, 255, 255)

        self.fontTime = ImageFont.truetype("fonts/Mecha.ttf", 17)

    def draw(self, draw, offset=0, tiles=1, brightness=255):
        offset = 32 * offset
        width = 32 * tiles

        #draw.rectangle((offset, 0, offset, 31), fill=scaleColor((255, 8, 8), brightness))
        #draw.rectangle((offset + width - 1, 0, offset + width - 1, 31), fill=scaleColor((8, 8, 255), brightness))

        colorTime = scaleColor(self.colorDay, brightness)
        if (time.strftime("%p") == "PM"):
            colorTime = scaleColor(self.colorNight, brightness)

        textTime = time.strftime("%I:%M")
        textWidth = self.fontTime.getsize(textTime)[0]
        draw.text((offset + ((width - textWidth) / 2), 0), textTime, font=self.fontTime, fill=colorTime)

        textToday = time.strftime("%A")
        textWidth = fontPixelMillennium.getsize(textToday)[0]
        draw.text((offset + ((width - textWidth) / 2), 16), textToday, font=fontPixelMillennium, fill=scaleColor(self.colorToday, brightness))

        textDate = time.strftime("%b %d")
        textWidth = fontPixelMillennium.getsize(textDate)[0]
        draw.text((offset + ((width - textWidth) / 2), 24), textDate, font=fontPixelMillennium, fill=scaleColor(self.colorDate, brightness))
