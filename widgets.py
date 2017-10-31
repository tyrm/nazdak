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
        self.colorToday = (0, 255, 0)
        self.colorDate = (255, 255, 255)

        self.fontTime = ImageFont.truetype("fonts/Mecha.ttf", 17)
        self.dateTime = ImageFont.truetype("fonts/PixelMillennium.ttf", 8)

    def draw(self, offset=0, tiles=1, brightness=25):
        offset = 32 * offset
        width = 32 * tiles

        #self.d.rectangle((offset, 0, offset, 31), fill=scaleColor((255, 8, 8), brightness))
        #self.d.rectangle((offset + width - 1, 0, offset + width - 1, 31), fill=scaleColor((8, 8, 255), brightness))

        colorTime = scaleColor(self.colorDay, brightness)
        if (time.strftime("%p") == "PM"):
            colorTime = scaleColor(self.colorNight, brightness)

        textTime = time.strftime("%I:%M")
        textWidth = self.fontTime.getsize(textTime)[0]
        self.d.text(((width - textWidth) / 2, 0), textTime, font=self.fontTime, fill=colorTime)

        textToday = time.strftime("%A")
        textWidth = self.dateTime.getsize(textToday)[0]
        self.d.text(((width - textWidth) / 2, 16), textToday, font=self.dateTime, fill=scaleColor(self.colorToday, brightness))

        textDate = time.strftime("%b %d")
        textWidth = self.dateTime.getsize(textDate)[0]
        self.d.text(((width - textWidth) / 2, 24), textDate, font=self.dateTime, fill=scaleColor(self.colorDate, brightness))
