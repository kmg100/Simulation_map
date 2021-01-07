#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 15:09:33 2020

@author: kristaps
"""

from PIL import Image,ImageDraw
#from numpy import mgrid, sum
import numpy as np



def CoM(image): 
    im = Image.open(image)
    imm = im.load()
    (X, Y) = im.size
    m = np.zeros((X, Y))
    
    m = np.sum(np.asarray(im), -1) < 255*3
    m = m / np.sum(np.sum(m))
    
    dx = np.sum(m, 0) 
    dy = np.sum(m, 1) 
    
    # expected values
    cx = np.sum(dx * np.arange(X))
    cy = np.sum(dy * np.arange(Y))
    draw = ImageDraw.Draw(im)
    draw.text((cx, cy),text="x")
    im.show()
    print(cx,cy)
    return cx,cy

if __name__ == "__main__":
    CoM("test.png")
