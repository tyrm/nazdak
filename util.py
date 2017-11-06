#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import logging
import requests

class AutoBrightness:
    def __init__(self, briDay=200, briNight=100, briSleep=32, sunPhaseApi="http://svc.pup.haus:4287/weather/sun_phase/v1"):
        self.briDay = briDay
        self.briNight = briNight
        self.briSleep = briSleep

        self.sunPhaseApi = sunPhaseApi

        self.timeSleepH = 23
        self.timeSleepM = 59

        self.dataM = -1 # Month of Sun data
        self.dataD = -1 # Data of Sun data
        self.sunriseH = -1
        self.sunriseM = -1
        self.sunsetH = -1
        self.sunsetM = -1

        self.lastUpdateM = -1

        self.brightness = 0

        self.updateData()

    def updateData(self):
        try:
            get_headers = {'Accept': 'application/vnd.api+json'}
            r = requests.get(self.sunPhaseApi, headers=get_headers)
            response = r.json()

            id = response["data"]["id"].split(':')
            dataDate = id[-1].split('-')

            self.dataM = dataDate[1]
            self.dataD = dataDate[2]
            self.sunriseH = response["data"]["attributes"]["sunrise_h"]
            self.sunriseM = response["data"]["attributes"]["sunrise_m"]
            self.sunsetH = response["data"]["attributes"]["sunset_h"]
            self.sunsetM = response["data"]["attributes"]["sunset_m"]

            logging.debug("Updated sun phase data. sunrise[{0}:{1}] sunset[{2}:{3}]".format(self.sunriseH, self.sunriseM, self.sunsetH, self.sunsetM))

        except:
            logging.error("Could not get updated Sun Phase data from Services.")

    def getBrightness(self):
        now = datetime.datetime.now()

        # Update values
        if now.minute != self.lastUpdateM:
            if datetime.time(self.sunriseH, self.sunriseM) <= now.time() < datetime.time(self.sunsetH, self.sunsetM):
                logging.debug("Updating Brightness Day")
                self.brightness = self.briDay
            elif datetime.time(self.sunsetH, self.sunsetM) <= now.time() < datetime.time(self.timeSleepH, self.timeSleepM):
                logging.debug("Updating Brightness Night")
                self.brightness = self.briNight
            else:
                logging.debug("Updating Brightness Sleep")
                self.brightness = self.briSleep
            self.lastUpdateM = now.minute

        return self.brightness

def scaleInt(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def scaleColor(c, b):
    scaledR = scaleInt(b, 0, 255, 0, c[0])
    scaledG = scaleInt(b, 0, 255, 0, c[1])
    scaledB = scaleInt(b, 0, 255, 0, c[2])

    return (scaledR, scaledG, scaledB)
