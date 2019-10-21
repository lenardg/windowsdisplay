#!/usr/bin/env python

import colorsys
import time
from random import randint
import blinkt

spacing = 360.0 / 16.0
hue = 0

blinkt.set_clear_on_exit()
blinkt.set_brightness(1.0)

def blueLilac():
    start = time.time()
    duration = randint(20,45)
    while True:
        current = time.time() % 30
        if current >= 15:
            current = 30 - current
        current = current * 3
        hue = current + 240  #int(time.time() * 100) % 360
        for x in range(blinkt.NUM_PIXELS):
            h = ((hue) % 360) / 360.0
            r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, r, g, b)

        blinkt.show()
        time.sleep(0.5)

        if time.time() - start > duration:
            break
 
def orangeRed():
    start = time.time()
    duration = randint(20,45)
    while True:
        current = time.time() % 30
        if current >= 15:
            current = 30 - current
        hue = current  #int(time.time() * 100) % 360
        for x in range(blinkt.NUM_PIXELS):
            h = ((hue) % 360) / 360.0
            r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, r, g, b)

        blinkt.show()
        time.sleep(0.5)

        if time.time() - start > duration:
            break
        
def blink():
    start = time.time()
    duration = randint(3,8)
    while True:
        blinkt.set_all(255,255,255)
        blinkt.show()
        time.sleep(0.01)
        blinkt.clear()
        blinkt.show()
        time.sleep(0.01)
        if time.time() - start > duration:
            break

try:
    while True:
        utcnow = time.gmtime()
        helnow = time.localtime()
        canBlink = True
        if utcnow.tm_hour < 15:   # we do not turn on before 15:00 UTC
            time.sleep(60)
            continue
        elif helnow.tm_hour >= 23: # at 23:00 local time we turn off
            break
        elif helnow.tm_hour >= 20: # after 20:00 local time we do not blink 
            canBlink = False

        if canBlink:
            blink()
        
        blueLilac()

        if canBlink:
            blink()

        orangeRed()

except KeyboardInterrupt:
    print("Keyboard break received")

blinkt.clear()
blinkt.show()
print("THE END.")

