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

########################
# CONSTANTS
########################
STATE_IDLE = 0
STATE_MORNING_BLINK = 7
STATE_MORNING_NOBLINK = 6
STATE_EVENING_BLINK = 18
STATE_EVENING_NOBLINK = 20

#########################
# Some more constants
#########################
spacing = 360.0 / 16.0
hue = 0

# the colors we use for blinking
blinkColors = [(255,255,255),(255,255,255),(255,255,255),(255,64,0),(192,0,255)]

xmasColors1 = [(255,255,255),(255,128,0),(0,255,0),(255,0,0)]
xmasColors2 = [(255,255,255),(255,0,255),(128,0,255),(0,0,255)]
xmasColors3 = [(255,200,0),(255,0,255),(0,255,0),(255,0,0)]

xmas = [xmasColors1, xmasColors2, xmasColors3]

# The program
program = [
    # CurrentState, WeekDayOnly, LocalHour, LocalMinute, MaxLocalHour, NewState
    [ STATE_IDLE, False, 6, 0, 8, STATE_MORNING_NOBLINK ],
    [ STATE_MORNING_NOBLINK, True, 6, 45, 9, STATE_MORNING_BLINK ],
    [ STATE_MORNING_NOBLINK, False, 8, 45, 9, STATE_IDLE ],
    [ STATE_MORNING_BLINK, False, 8, 45, 9, STATE_IDLE ],
    
    # Afternoon
    [ STATE_IDLE, False, 15, 20, 23, STATE_EVENING_BLINK ],
    [ STATE_EVENING_BLINK, False, 19, 30, -1, STATE_EVENING_NOBLINK ],
    [ STATE_EVENING_NOBLINK, False, 23, 45, -1, STATE_IDLE ]
]

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
        if saturation <= 0.2:
            saturation = 0.2
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

    thisBlink = choice(xmas)

    while True:
        r, g, b = choice(thisBlink)
        blinkt.set_all(r, g, b)
        blinkt.show()
        time.sleep(1)
        if time.time() - start > duration:
            break
    clear()
  
def lightshow(canBlink):
    if canBlink:
        xmasblink()
    whiteOrange()
    if canBlink:
        xmasblink()
    orangeRed()

#######################
# MAIN
########################
try:
    print("CHRISTMAS lights")
    state = STATE_IDLE
                # states: 
                #   0 not running
                #   6 morning run without blink
                #   7 morning run with blink 
                #  18 night run with blink
                #  20 night run without blink

    debugtime = 1607243275 - 3600 * 5 # 1572112625 # 1571882400 
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

        # process the program
        for p in program:
            if p[0] == state: # if this rule applies in this state
                if p[1] and helnow.tm_wday > 4: # if this rule applies on weekdays only, skip on weekends
                    continue
                if p[2] < helnow.tm_hour or (p[2] == helnow.tm_hour and p[3] < helnow.tm_min):
                    if p[4] >= 0 and p[4] <= helnow.tm_hour:
                        continue
                    state = p[5]
                    print("Current time is: {0}:{1}, new state {2}".format(helnow.tm_hour, helnow.tm_min, state))

        # process the state
        if state == STATE_MORNING_BLINK or state == STATE_EVENING_BLINK:
            canBlink = True
        else:
            canBlink = False

        if state == STATE_IDLE:
            if debug:
                print("{0}-{1}-{2} {3}:{4} Idle".format(helnow.tm_year, helnow.tm_mon, helnow.tm_mday, helnow.tm_hour, helnow.tm_min))
            else:
                time.sleep(60)
        else:
            if debug:
                print("{0}-{1}-{2} {3}:{4} Lightshow, state={5}, canBlink={6}".format(helnow.tm_year, helnow.tm_mon, helnow.tm_mday, helnow.tm_hour, helnow.tm_min, state, canBlink))
            else:
                lightshow(canBlink)

except KeyboardInterrupt:
    print("Keyboard break received")

clear()
print("THE END.")

