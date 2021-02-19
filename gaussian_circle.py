#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 13:16:41 2021

@author: kristaps
drawing ellipse
"""

import cv2
import numpy as np
import math


# ============================================================================
#logs kura tiek iezīmēta bilde 
def ellipse_bbox(h, k, a, b, theta):
    ux = a * math.cos(theta)
    uy = a * math.sin(theta)
    vx = b * math.cos(theta + math.pi / 2)
    vy = b * math.sin(theta + math.pi / 2)
    box_halfwidth = np.ceil(math.sqrt(ux**2 + vx**2))
    box_halfheight = np.ceil(math.sqrt(uy**2 + vy**2))
    return ((int(h - box_halfwidth), int(k - box_halfheight))
        , (int(h + box_halfwidth), int(k + box_halfheight)))

# ----------------------------------------------------------------------------

# Rotated elliptical gradient FORMULA pec kuras aprekinas katra pikseļa vertiba no 0 lidz 255 pedejais width
def make_gradient(width, height, h, k, a, b, theta):
    # Precalculate constants
    st, ct =  math.sin(theta), math.cos(theta)
    aa, bb = a**2, b**2
        
    # Generate (x,y) coordinate arrays
    y,x = np.mgrid[-k:height-k,-h:width-h]
    # Calculate the weight for each pixel
    weights = ((((x) * ct + (y) * st) ** 2) / aa) + ((((x) * st - (y) * ct) ** 2) / bb)
    #print(weights.shape)
    return np.clip(weights, 0 , 1)

# ============================================================================ 

def draw_image(a, b, theta, inner_scale):
    # aprēķini lai elipse butu centrēta
    _, (h, k) = ellipse_bbox(0,0,a,b,theta) # Ellipse center
    h += 2 # Add small margin
    k += 2 # Add small margin
    width, height = (h*2+1, k*2+1) # Canvas size

    # Parameters defining the two ellipses for OpenCV (a RotatedRect structure)
    ellipse_outer = ((h,k), (a*2, b*2), math.degrees(theta))
    ellipse_inner = ((h,k), (a*2*inner_scale, b*2*inner_scale), math.degrees(theta))

    # ģenerē ārpus elipses transperant backgroundu
    transparency = np.zeros((height, width), np.uint8)
    cv2.ellipse(transparency, ellipse_outer, 255, -1, cv2.LINE_AA)
    
    # uzģenerē graianta saturu 8bit pelekai rainagm
    intensity = np.uint8((make_gradient(width, height, h, k, a, b, theta) * 255)-a)#a ofsets ir lai gradiants saktos no iekšējās elipses
    cv2.imwrite("inn.png", intensity)
    # Uzzimē iekšejo elipsi un padara viņu caurspīdīgu
    cv2.ellipse(intensity, ellipse_inner, 255, -1, cv2.LINE_AA)
    cv2.ellipse(transparency, ellipse_inner, 0, -1, cv2.LINE_AA)#visu balto padara transperant

    # Turn it into a BGRA image
    result = cv2.merge([intensity, intensity, intensity, transparency])
    return result

# ============================================================================ 

a, b = (50.0, 50.0) # Radiusu izmēri
theta = math.radians(0.0) # Riņķa rotācija  (radians)
inner_scale = 0.6 # Cik biezs ir rinķis
    
cv2.imwrite("eligrad.png", draw_image(a, b, theta, inner_scale))
