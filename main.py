#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:00:42 2020

@author: kristaps
"""
import matplotlib
matplotlib.use("TkAgg")
import math
import time
import numpy as np
import random
from matplotlib import pyplot as plt

class PathLoss:
    def __init__(self, P: float, fc: float, Ox: int, Oy: int, mode: str,**kwargs: any):
        """
        Initializes the path loss object.
        Parameters
        Ox:Raiditijaa atrasanas vietas x 
        Oy:Raiditijaa atrasanas vietas y
        available modes are static, linear, circular or reset
        """
        self.area_type:str ='open'
        for key, value in kwargs.items(): 
            if key == "Ax":
                self.Ax:int=value
            elif key == "Ay": 
                self.Ay:int=value
            elif key == "Bx": 
                self.Bx:int=value
            elif key == "By": 
                self.By:int=value
            elif key == "v": 
                self.v:float=value
            elif key == "envo": 
                self.area_type:str = value

        
        self.stst_mode =False
        self.lin_mode =False
        self.circ_mode =False
        self.tel_mode =False
        self.Ox: int = Ox
        self.Oy: int = Oy
        #start_time = time.time()
        self.P: float = P         #dota jauda
        self.fc: float = fc       #dota frekvence
        self.mode: str = mode     #viena no cetram funkcijam

            
        if mode == "static":
            print("Static mode with:"+' Frequency-'+str(self.fc)+"GHz"+ ", antenna coords-"+str(self.Ax)+","+str(self.Ay)+" , recording coords-"+str(self.Bx)+","+str(self.By))
            self.stst_mode =True
        elif self.mode == "linear":
            print("Linear mode with:"+' Frequency-'+str(self.fc)+"GHz"+ ", walking strting coords-"+str(self.Ax)+","+str(self.Ay)+" , end coords-"+str(self.Bx)+","+str(self.By)+" , speed-"+str(self.v))
            self.lin_mode =True
            self.radians = math.atan2(abs(self.By)-self.Ay, abs(self.Bx)-self.Ax)
            self.Vy=self.v*math.cos(self.radians)
            self.Vx=self.v*math.sin(self.radians)
            self.newAx = self.Ax
            self.newAy = self.Ay
            self.back = False
        elif self.mode == "circular":
            print("Circular mode with:"+'Frequency-'+str(self.fc)+", with the centre at- "+str(self.Ax)+","+str(self.Ay)+",distance in x-"+str(self.Bx)+",distance in y-"+str(self.By)+" , speed-"+str(self.v))
            self.circ_mode =True
            self.angle = math.radians(1)
            self.Ex = self.Ax + self.Bx * (math.cos(self.angle))#starting coords
            self.Ey = self.Ay + self.By * (math.sin(self.angle))
            print(self.Ax,self.Ay)
        elif self.mode == "teleport":
            self.tel_mode =True
            print("Teleport mode with:"+'Frequency-'+str(self.fc))
            
        elif self.mode == "reset":
            self.stst_mode =False
            self.lin_mode =False
            self.circ_mode =False
            self.tel_mode =False
            print("reset")
        else:
            raise RuntimeError("Not valid keyword")
            
        if self.fc < 0.0 or self.fc > 20000.0:
            msg = ("The carrier frequency is out of range")
            raise RuntimeError(msg)
            
            

    def calc_distance(self,x1,y1,x2,y2):
        self.x_dist = (x2 - x1)
        self.y_dist = (y2 - y1)
        self.d = math.sqrt(self.x_dist * self.x_dist + self.y_dist * self.y_dist)
        return self.d
        ##calculats the distance between two antennas
        
    def calc_loss(self):
        if self.stst_mode == True:
            self.calc_distance(self.Ox,self.Oy,self.Ax,self.Ay)
            self.K = self._calc_K()
            self.pl = 10*self.K*(math.log10(self.d))+20*(math.log10(self.fc))+92.45#gigaherz and kilometeres
            print("The loss is %.2f dB" % self.pl)
        else:
            raise RuntimeError("Static mode not initialised")
        return self.pl
    
    def lin_moving(self):#v is speed seit ka parvietojas ar konstantu atrumu no punkta uz punktu un atpakal
        #when called calculate the new loss
        #if self.newAx <= self.Bx and self.newAy <= self.By and self.start == True:
        
            #print("start of road, moving forwords")
        if self.lin_mode == True:
            if self.newAx <= self.Ax and self.newAy <= self.Ay:
                print("start of road, moving forwords")
                self.back = False
            if self.newAx >= self.Bx and self.newAy >= self.By:
                print("end of road, moving backwords")
                self.back = True
            if self.back == True:
                self.newAx -= self.Vx
                self.newAy -= self.Vy
                self.K = self._calc_K()
                self.calc_distance(self.Ox,self.Oy,self.newAx,self.newAy)
                self.pl = 10*self.K*(math.log10(self.d))+20*(math.log10(self.fc))+92.45#gigaherz and kilometeres
                print("The loss is %.2f dB" % self.pl)
                #time.sleep(1)
            else:
                self.newAx += self.Vx
                self.newAy += self.Vy
                #print(self.newAx)
                self.calc_distance(self.Ox,self.Oy,self.newAx,self.newAy)
                self.K = self._calc_K()
                self.pl = 10*self.K*(math.log10(self.d))+20*(math.log10(self.fc))+92.45#gigaherz and kilometeres
                print("The loss is %.2f dB" % self.pl)
                #time.sleep(1)
        else:
            raise RuntimeError("Linear mode not initialised")
        return self.newAx,self.newAy
            
    def elip_moving(self):
        if self.circ_mode == True:
            self.Ex=self.Ex+self.Bx*self.v*math.cos(self.angle+(math.pi/2))
            self.Ey=self.Ey+self.By*self.v*math.sin(self.angle+(math.pi/2))
            self.calc_distance(self.Ox,self.Oy,self.Ex,self.Ey)
            self.K = self._calc_K()
            self.pl = 10*self.K*(math.log10(self.d))+20*(math.log10(self.fc))+92.45#gigaherz and kilometeres
            print("The loss is %.2f dB" % self.pl)
            self.angle += self.v
            time.sleep(1)
        else: 
            raise RuntimeError("Circular mode not initialised")
        return self.Ex,self.Ey
            
    def teleport(self, maxdist,sleeptime):
        if self.tel_mode == True:
            self.Tx = random.randint(0,maxdist)
            self.Ty = random.randint(0,maxdist)
            self.calc_distance(self.x1,self.y1,self.Tx,self.Ty)
            self.K = self._calc_K()
            self.pl = 10*self.K*(math.log10(self.d))+20*(math.log10(self.fc*10**9))+92.45#gigaherz and kilometeres
            print("The loss is %.2f dB" % self.pl)
            time.sleep(sleeptime)
        else: 
            raise RuntimeError("Teleport mode not initialised")
    def reset(self):
        self.__init__(self.P, self.fc,Ax = 0, Ay = 0,Bx = 0,By = 0,v =  0, mode = "reset",envo="open")
############Vides izvelesanas
    def _calc_K(self) -> float:
        """
        Calculates the "'City'/'Forest'/'Open'" correction
        factor.
        Returns
        -------
        K : float
            The correction factor "K".
        """
        if self.area_type == 'city':
            K = 2.7
        elif self.area_type == 'open':
            K = 2
        elif self.area_type == 'forest':
            K = 3
        else:
            K = 2
        return K

if __name__ == "__main__":
        
    a = PathLoss(1000.0, 60, 0,0,Ax = -100, Ay = -100,Bx = -400, By = -400,v = 10,mode = "linear", envo="forest")#nestrada ar negativiem skaitliem
    """fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    line, = ax1.plot([], lw=3)
    fig.canvas.draw()  
    plt.plot
    array=[]"""
    
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    x = []
    y = []
    ax1.set_xlim(-1000, 1000)
    ax1.set_ylim(-1000, 1000)
    line, = ax1.plot([], lw=3)
    fig.canvas.draw()  
    plt.show(block=False)
    #plt.show()#a.calc_loss()
    for i in range(0,600):
        ax,ay = a.lin_moving()
        x.append(ax)
        y.append(ay)
        ax1.plot(x, y, '-ok',color='black')
        fig.canvas.draw()
        #plt.plot(x, y, '-ok',color='black')
        #print(ax,ay)
        #plt.scatter(ax,ay)#
        fig.canvas.flush_events()
    #print(x,y)
    


    
#    a.elip_moving()
    #a.teleport(1000, 1.0)
#a.reset()