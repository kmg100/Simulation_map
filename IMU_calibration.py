#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 14:21:01 2021

@author: kristaps
"""
import time
 
import board
import busio
 
# import digitalio # Used with SPI
import adafruit_lsm9ds0
import math

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)

#range for the values
running_mmin = (32767, 32767, 32767)
running_mmax = (-32768, -32768, -32768)
running_amin = (32767, 32767, 32767)
running_amax = (-32768, -32768, -32768)

measuring_duration = 15.0 # units are seconds

print('Calibrating magnetometer X, Y, Z axis values, move slowly in figure 8 and rotate...')
start_time = time.time()
while (time.time() < start_time + measuring_duration):
    # Read the X, Y, Z axis magnetometer and acceleration values 
    mag = sensor.magnetic#read the 3 axis values
    # Grab the X, Y, Z components from the reading for printing.
    mag_x, mag_y, mag_z = sensor.magnetic
    # set lowest and highest values seen so far
    running_mmin = tuple(map(lambda x, y: min(x,y), running_mmin, mag))
    running_mmax = tuple(map(lambda x, y: max(x,y), running_mmax, mag))
    
    print('Mag X={0}, Mag Y={1}, Mag Z={2}'.format(
          mag_x, mag_y, mag_z))
    print('mag minimums: ',running_mmin)
    print('mag maximums: ',running_mmax)
    # Wait 1/10th of a second and repeat.
    time.sleep(0.1)
    
    
    
moffset = tuple(map(lambda x1, x2: (x1+x2) / 2., running_mmin, running_mmax))
avg_mdelta = tuple(map(lambda x1, x2: (x2-x1)/2., running_mmin, running_mmax))
combined_avg_mdelta = (avg_mdelta[0] + avg_mdelta[1] + avg_mdelta[2])/3.
scale_mx = combined_avg_mdelta / avg_mdelta[0]
scale_my = combined_avg_mdelta / avg_mdelta[1]
scale_mz = combined_avg_mdelta / avg_mdelta[2]
print('magnetometer offsets: ',moffset)
print('magentometer scaling: ',scale_mx, scale_my, scale_mz)
