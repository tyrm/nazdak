#!/usr/bin/env python
# -*- coding: utf-8 -*-

def scaleInt(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def scaleColor(c, b):
    scaledR = scaleInt(b, 0, 100, 0, c[0])
    scaledG = scaleInt(b, 0, 100, 0, c[1])
    scaledB = scaleInt(b, 0, 100, 0, c[2])

    return (scaledR, scaledG, scaledB)
