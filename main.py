#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:00:42 2020

@author: kristaps
"""
import math
import time


class PathLoss:
    def __init__(self, P: float, fc: float, Ax:int,Ay:int,Bx:int,By:int,v:float,mode: str):
        """
        Initializes the path loss object.
        Parameters
        """
        self.x1=0
        self.y1=0
        #start_time = time.time()
        self.P: float = P #dota jauda
        self.fc: float = fc #dota frekvence
        self.mode: str = mode
        self.Bx:int = Bx
        self.By:int=By
        self.Ax:int=Ax
        self.Ay:int=Ay
        self.v:float = v
        if mode == "static":
            print("static mode")
        elif self.mode == "linear":
            print("linear mode")
            self.radians = math.atan2(By-Ay, Bx-Ax)
            self.Vy=v*math.cos(self.radians)
            self.Vx=v*math.sin(self.radians)
            self.newAx = Ax
            self.newAy = Ay
            self.back = False
        elif self.mode == "circular":
            self.angle = math.radians(90)
            self.Ex = self.Ax + self.Bx + (math.cos(self.angle))#starting coords
            self.Ey = self.Ay + self.By + (math.sin(self.angle))
        elif self.mode == "reset":
            print("reset")
            
            
            
    def calc_distance(self,x1,y1,x2,y2):
        self.x_dist = (x2 - x1)
        self.y_dist = (y2 - y1)
        self.d = math.sqrt(self.x_dist * self.x_dist + self.y_dist * self.y_dist)
        return self.d
        ##calculats the distance between two antennas
        
    def calc_loss(self,x2,y2):
        self.calc_distance(self.x1,self.y1,x2,y2)
        self.pl = 20*(math.log10(self.d))+20*(math.log10(self.fc))+92.45#gigaherz and kilometeres
        print("The loss is %.2f dB" % self.pl)
        return self.pl
    
    def lin_moving(self):#v is speed seit ka parvietojas ar konstantu atrumu no punkta uz punktu un atpakal
        #when called calculate the new loss
        #if self.newAx <= self.Bx and self.newAy <= self.By and self.start == True:
            
            #print("start of road, moving forwords")
        if self.newAx <= self.Ax and self.newAy <= self.Ay:
            print("start of road, moving forwords")
            self.back = False
        if self.newAx >= self.Bx and self.newAy >= self.By:
            print("end of road, moving backwords")
            self.back = True
        if self.back == True:
            self.newAx -= self.Vx
            self.newAy -= self.Vy
            self.calc_distance(self.x1,self.y1,self.newAx,self.newAy)
            self.pl = 20*(math.log10(self.d))+20*(math.log10(self.fc))+92.45#gigaherz and kilometeres
            print("The loss is %.2f dB" % self.pl)
            time.sleep(1)
        else:
            self.newAx += self.Vx
            self.newAy += self.Vy
            #print(self.newAx)
            self.calc_distance(self.x1,self.y1,self.newAx,self.newAy)
            self.pl = 20*(math.log10(self.d))+20*(math.log10(self.fc))+92.45#gigaherz and kilometeres
            print("The loss is %.2f dB" % self.pl)
            time.sleep(1)
    def elip_moving(self):
        self.Ex=self.Ex+self.Bx*self.v*math.cos(self.angle+(math.pi/2))
        self.Ey=self.Ey+self.By*self.v*math.sin(self.angle+(math.pi/2))
        self.calc_distance(self.x1,self.y1,self.Ex,self.Ey)
        self.pl = 20*(math.log10(self.d))+20*(math.log10(self.fc))+92.45#gigaherz and kilometeres
        print("The loss is %.2f dB" % self.pl)
        self.angle += self.v
        time.sleep(1)
    def teleport(self):
        pass
    def reset(self):
        self.__init__(self.P, self.fc,0, 0, 0, 0, 0, "reset")
############Vides izvelesanas
    def _calc_K(self) -> float:
        """
        Calculates the "'medium city'/'suburban'/'open area'" correction
        factor.
        Returns
        -------
        K : float
            The correction factor "K".
        """
        if self.area_type == 'large city':
            K = 0.0
        elif self.area_type == 'open':
            # Value for 'open' areas
            # $K = 4.78 (\log(f))^2 - 18.33 \log(f) + 40.94$
            K = (4.78 * (math.log10(self.fc)**2) -
                 18.33 * math.log10(self.fc) + 40.94)
        elif self.area_type == 'suburban':
            # Value for 'suburban' areas
            # $K = 2 [\log(f/28)^2] + 5.4$
            K = 2 * (math.log10(self.fc / 28.0)**2) + 5.4
        else:
            K = 0
        return K
    
a = PathLoss(1000.0, 60000, 100, 100,300,100,0.1,mode = "circular")
a.calc_loss(200, 200)
for i in range(0,366):
    #a.lin_moving()
    a.elip_moving()
a.reset()
