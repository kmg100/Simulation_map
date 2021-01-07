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
    """
    This Function calculates the centre coordiants of a image 
    returns cx and cy as float numbers
    """
    im = Image.open(image) #opens the image
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
    draw.text((cx, cy),text="x")#draws an x at the centre of the image
    im.show()
    print(cx,cy)
    return cx,cy

if __name__ == "__main__":
    CoM("test.png")
