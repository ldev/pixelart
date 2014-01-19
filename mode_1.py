#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from time import sleep
from random import randint
from math import ceil

number_of_pixels = 48
simultaneously_changing = 10
unused_leds_start = 2

# returns a random target with a list of R, G and B
def create_target():
    data = []
    
    # mix it up with black pixels
    if(randint(0,10)%5 == 0):
        data = [0, 0, 0]
    else:
        for x in range(0, 3):
            data.append(randint(0,255))
    return data

# choose a random pixel. Will not select the pixels already in use
def choose_random_pixel(currenly_used_pixels):
    while True:
        x = randint(0, number_of_pixels-1)
        if(x not in currenly_used_pixels):
            return x

# fade between colors
def fade_step(current, target, divider = 10):
    if(set(current) == set(target)):
        return False
    else:
        # Red
        if(current[0] < target[0]):
            current[0] += int(ceil((target[0]-current[0])/divider))
            
        elif(current[0] > target[0]):
            current[0] -= int(ceil((current[0]-target[0])/divider))

        # Green
        if(current[1] < target[1]):
            current[1] += int(ceil((target[1]-current[1])/divider))
        elif(current[1] > target[1]):
            current[1] -= int(ceil((current[1]-target[1])/divider))

        # Blue
        if(current[2] < target[2]):
            current[2] += int(ceil((target[2]-current[2])/divider))
        elif(current[2] > target[2]):
            current[2] -= int(ceil((current[2]-target[2])/divider))
        
        return current
    
spidev = file("/dev/spidev0.0", "wb")

# initialize the dataset - start with all black
pixelmap = []
for x in range(0, number_of_pixels):
    pixelmap.append([0, 0, 0])

targets = {}

while True:
    if(len(targets) < simultaneously_changing):
        while len(targets) < simultaneously_changing:
            new_pixel = choose_random_pixel(pixelmap)
            targets[new_pixel] = create_target()

    # loop over the dataset
    for pixel, colors in targets.items():
        step = fade_step(pixelmap[pixel], colors)
        if(step == False):
            del targets[pixel]
        else:
            pixelmap[pixel] = step
    
        
    # write to LEDs
    data = ''
    for led in pixelmap:
        data += chr(led[0])+chr(led[1])+chr(led[2])

    spidev.write(bytearray(b'\x00\x00\x00'*unused_leds_start)+data)
    spidev.flush()
    sleep(0.002)
	
