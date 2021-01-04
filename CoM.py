#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 15:09:33 2020

@author: kristaps
"""

from PIL import Image
import numpy as np

im = Image.open('image.bmp')
immat = im.load()
(X, Y) = im.size
m = np.zeros((X, Y))

m = np.sum(np.asarray(im), -1) < 255*3
m = m / np.sum(np.sum(m))

dx = np.sum(m, 0) # there is a 0 here instead of the 1
dy = np.sum(m, 1) # as np.asarray switches the axes, because

# expected values
cx = np.sum(dx * np.arange(X))
cy = np.sum(dy * np.arange(Y))
im.show()
print(cx,cy)