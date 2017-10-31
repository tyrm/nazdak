#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os

from PIL import ImageFont

from util import scaleColor

#defaultFont   = ImageFont.load(os.path.dirname(os.path.realpath(__file__)) + '/helvR08.pil')
class Clock:
    def __init__(self, d):
        self.d = d

        self.colorDay = (255, 255, 128)
        self.colorNight = (128, 128, 255)

        self.fontTime = ImageFont.truetype("fonts/Mecha.ttf", 17)
        self.dateTime = ImageFont.truetype("fonts/PixelMillennium.ttf", 8)

    def draw(self, offset=0, tiles=1, brightness=25):
        offset = 32 * offset
        width = 32 * tiles

        self.d.rectangle((offset, 0, offset, 31), fill=scaleColor((255, 8, 8), brightness))
        self.d.rectangle((offset + width - 1, 0, offset + width - 1, 31), fill=scaleColor((8, 8, 255), brightness))

        colorTime = scaleColor(self.colorDay, brightness)
        if (time.strftime("%p") == "PM"):
            colorTime = scaleColor(self.colorNight, brightness)

        textTime = time.strftime("%I:%M")
        textWidth = self.fontTime.getsize(textTime)[0]
        self.d.text(((width - textWidth) / 2, 0), textTime, font=self.fontTime, fill=colorTime)

        textDate = time.strftime("%a %d")
        textWidth = self.dateTime.getsize(textDate)[0]
        self.d.text(((width - textWidth) / 2, 18), textDate, font=self.dateTime, fill=colorTime)
