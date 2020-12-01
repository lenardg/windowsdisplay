#!/usr/bin/env python

##############################################################
# Christmas lights for window display
# uses Blinkt! library
#
# by Lenard Gunda
##############################################################

import colorsys
import time
from random import randint, choice
import blinkt

spacing = 360.0 / 16.0
hue = 0

# the colors we use for blinking
blinkColors = [(255,255,255),(255,255,255),(255,255,255),(255,64,0),(192,0,255)]

xmasColors = [(255,255,255),(255,128,0),(0,255,0),(255,0,0)]

# Set to True to see time values. Set to False (default) for normal operation
debug = False

# setup
if not debug:
    blinkt.set_clear_on_exit()
    blinkt.set_brightness(1.0)

########################
# Functions
########################

# clear the lights
def clear():
    if not debug:
        blinkt.clear()
        blinkt.show()

def colorfade(minSeconds, maxSeconds, shift = 0, multiplier = 1.0, fullRange = 30):
    start = time.time()
    duration = randint(minSeconds, maxSeconds)
    while True:
        current = time.time() % fullRange
        if current >= fullRange / 2:
            current = fullRange - current
        current = current * multiplier
        hue = current + shift 
        for x in range(blinkt.NUM_PIXELS):
            h = ((hue) % 360) / 360.0
            r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, r, g, b)

        blinkt.show()
        time.sleep(0.5)

        if time.time() - start > duration:
            break
 
def saturationfade(minSeconds, maxSeconds, shift = 0, multiplier = 1.0, fullRange = 30):
    start = time.time()
    duration = randint(minSeconds, maxSeconds)
    saturation = 1.0
    satdir = -0.05
    while True:
        current = time.time() % fullRange
        if current >= fullRange / 2:
            current = fullRange - current
        current = current * multiplier
        hue = current + shift 

        saturation = saturation + satdir
        if saturation <= 0:
            saturation = 0.0
            satdir = 0.05
        elif saturation >= 1.0:
            saturation = 1.0
            satdir = -0.05

        for x in range(blinkt.NUM_PIXELS):
            h = ((hue) % 360) / 360.0
            r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, saturation, 1.0)]
            blinkt.set_pixel(x, r, g, b)

        blinkt.show()
        time.sleep(0.5)

        if time.time() - start > duration:
            break
 

def whiteOrange():
    saturationfade(20, 45, 20)
    #colorfade(20, 45)

def blueLilac():
    colorfade(20, 45, 240, 3.0)

def orangeRed():
    colorfade(20, 45)

def xmasblink():
    start = time.time()
    duration = randint(20,45)

    while True:
        r, g, b = choice(xmasColors)
        blinkt.set_all(r, g, b)
        blinkt.show()
        time.sleep(1)
        if time.time() - start > duration:
            break
    blinkt.clear()
    blinkt.show()
  
      
def blink():
    start = time.time()
    duration = randint(3,8)

    r, g, b = choice(blinkColors)

    while True:
        blinkt.set_all(r, g, b)
        blinkt.show()
        time.sleep(0.01)
        blinkt.clear()
        blinkt.show()
        time.sleep(0.01)
        if time.time() - start > duration:
            break

def lightshow(canBlink):
    if canBlink:
        xmasblink()
    whiteOrange()
    if canBlink:
        xmasblink()
    orangeRed()

########################
# CONSTANTS
########################
STATE_IDLE = 0
STATE_MORNING_BLINK = 7
STATE_MORNING_NOBLINK = 6
STATE_EVENING_BLINK = 18
STATE_EVENING_NOBLINK = 20

########################
# MAIN
########################
try:
    print("HALLOWEEN lights")
    state = STATE_IDLE
                # states: 
                #   0 not running
                #   6 morning run without blink
                #   7 morning run with blink 
                #  18 night run with blink
                #  20 night run without blink

    debugtime = 1572112625 # 1571882400 
    endtime = debugtime + 3600 * 32

    # begin state machine
    while True:
        if not debug:
            now = time.time()
        else:
            now = debugtime
            debugtime = debugtime + 60
            if debugtime > endtime:
                break

        utcnow = time.gmtime(now)
        helnow = time.localtime(now)

        # state transitions
        if state == STATE_IDLE:
            if helnow.tm_hour >= 6 and utcnow.tm_hour < 5:
                print("It's 6:00 local, we turn on")
                state = STATE_MORNING_NOBLINK
                continue
            elif (helnow.tm_hour > 16 or (helnow.tm_hour == 16 and helnow.tm_min > 30)) and helnow.tm_hour < 23:
                print("It's 16:30 local time, we turn on")
                state = STATE_EVENING_BLINK
                continue
            if not debug:
                time.sleep(60)
            else:
                print("{0}:{1} idle".format(helnow.tm_hour, helnow.tm_min))
            continue
        elif state == STATE_MORNING_NOBLINK:
            if helnow.tm_wday > 4:
                if utcnow.tm_hour > 5 or (utcnow.tm_hour == 5 and utcnow.tm_min > 24):
                    print("On weekdays we do not blink in the morning, but stop after 5:24 UTC, turn off lights")
                    state = STATE_IDLE
                    clear()
                    continue
            elif helnow.tm_hour > 6 or (helnow.tm_hour == 6 and helnow.tm_min > 45):
                print("After 6:45 local, blinking can start")
                state = STATE_MORNING_BLINK
                continue
        elif state == STATE_MORNING_BLINK:
            if utcnow.tm_hour > 5 or (utcnow.tm_hour == 5 and utcnow.tm_min > 45):
                print("It's after 5:45 UTC, turn off lights")
                state = STATE_IDLE
                clear()
                continue
        elif state == STATE_EVENING_BLINK:
            if helnow.tm_hour > 19 or (helnow.tm_hour == 19 and helnow.tm_min > 30):
                print("After 19:30 local, blinking will stop now")
                state = STATE_EVENING_NOBLINK
        elif state == STATE_EVENING_NOBLINK:
            if helnow.tm_hour > 23 or (helnow.tm_hour == 23 and helnow.tm_min > 45):
                print("It's 23:45 local, turn off lights")
                state = STATE_IDLE
                clear()
                continue

        if state == STATE_MORNING_BLINK or state == STATE_EVENING_BLINK:
            canBlink = True
        else:
            canBlink = False

        if debug:
            print("{0}:{1} Lightshow, canBlink={2}".format(helnow.tm_hour, helnow.tm_min, canBlink))
        else:
            lightshow(canBlink)

except KeyboardInterrupt:
    print("Keyboard break received")

clear()
print("THE END.")

