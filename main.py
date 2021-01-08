#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:00:42 2020

@author: Kristaps Greitans at EDI
This library simulates the free path loss value depending on several variables, the frequency is in GHZ and distance is in meters
"""
import matplotlib
matplotlib.use("TkAgg")
import math
import time
import random
from matplotlib import pyplot as plt
#from sys import exit

class PathLoss:
    """
    Initializes the path loss object.
    -----------------------------------------------------------
    Parameters:
        
    P: Power of the antenna
    
    fc: frequency of the antenna in GHz
    
    Ox:   Raiditija atrasanas vietas x metros
    
    Oy:   Raiditija atrasanas vietas y metros
    
    Mode: available modes are static, linear, circular or reset
    -----------------------------------------------------------
    Available arguments:
        
    Ax:   Starting x coordiantes for linear movement and the center x coordiantes for elyptical movement
    
    Ay:   Starting y coordiantes for linear movement and the center y coordiantes for elyptical movement
    
    Bx:   Finishing x coordiantes for linear movement and the displacement x coordiantes for elyptical movement
    
    By:   Finishing y coordiantes for linear movement and the displacement y coordiantes for elyptical movement
    
    v:    Movement speed for linear and elyptical movement in m/s
    
    envo: The enviroment for the simulation, if not specified then open (open)
    """
    def __init__(self, P: float, fc: float, Ox: int, Oy: int, mode: str,**kwargs: any):
        self.v = 1 #if no speed provided 1 m/s
        self.area_type:str ='open'
        #reading arguments
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
            else:
                raise RuntimeError("Wrong variable input %s" %key)
        #defining input variables
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
        
        ############Matplotlib variables and innit
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.dx = []
        self.dy = []
        self.ax1.set_xlim(-1000, 1000)
        self.ax1.set_ylim(-1000, 1000)
        self.line, = self.ax1.plot([], lw=3)
        self.ax1.plot(self.Ox,self.Oy, marker="D")
        #self.fig.canvas.draw()  
        
        #selecting mode depending on the input
        if mode == "static":
            print("Static mode with: Frequency: %.2f GHz, radiated antenna coordiantes (%3d,%3d) , Recieving antenna coordiantes: (%3d,%3d)" %(self.fc,self.Ox,self.Oy,self.Ax,self.Ay))
            #print("Static mode with:"+' Frequency:'+str(self.fc)+"GHz"+ ", antenna coords:"+str(self.Ax)+","+str(self.Ay)+" , recording coords:"+str(self.Bx)+","+str(self.By))
            self.stst_mode =True
        elif self.mode == "linear":
            if self.Ax ==self.Bx and self.Ay == self.By:
                msg = ("Start and End point same value")
                raise RuntimeError(msg)
            #optional method of tracking movement 
            #self.start_time = time.time()
            print("Linear mode with: Frequency: %.2f GHz, radiated antenna coordiantes (%3d,%3d) , walking starting coordiantes: (%3d,%3d), walking end coordiantes: (%3d,%3d), the walking speed: %2f m/s" %(self.fc,self.Ox,self.Oy,self.Ax,self.Ay,self.Bx,self.By,self.v))
            self.lin_mode =True
            self.radians = math.atan2(self.Bx-self.Ax, self.By-self.Ay)#starada pareizi
            self.Vx=self.v*math.cos(self.radians)
            self.Vy=self.v*math.sin(self.radians)
            self.start = True
            self.back = False
            self.newAx = self.Ax
            self.newAy = self.Ay
            
        elif self.mode == "circular":
            if self.Ax ==self.Bx and self.Ay == self.By:
                msg = ("Start and End point same value")
                raise RuntimeError(msg)
            self.ax1.plot(self.Ax,self.Ay, marker="D")
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
        self.d = 0.001*math.sqrt(self.x_dist * self.x_dist + self.y_dist * self.y_dist)#converts to Km for the equation
        #print(self.d*0.001)
        return self.d
        ##calculats the distance between two antennas
        
    def static(self):
        """
        Calculates the "Path space loss" for static case of the reciever antenna
        Returns
        -------
        pl : float
            path loss db value "pl".
        """
        if self.stst_mode == True:
            self.calc_distance(self.Ox,self.Oy,self.Ax,self.Ay)
            self.K = self._calc_K()
            self.pl = 10*self.K*(math.log10(self.d))+10*self.K*(math.log10(self.fc))+92.45#gigaherz and kilometeres
            print("The loss is %.2f dB" % self.pl)
        else:
            raise RuntimeError("Static mode not initialised")
        return self.pl
    
    def lin_moving(self):#v is speed seit ka parvietojas ar konstantu atrumu no punkta uz punktu un atpakal
        """
        Calculates the "Free space loss" for linear movement of the reciever antenna
        Returns
        -------
        pl : float
            path loss db value "pl".
        """
        if self.lin_mode == True:
            if self.start == True:
                #Optional to have the new location every time the function is called depending on the start time not every second
                ##self.newAx = self.Vx * (time.time()-self.start_time)
                ##self.newAy = self.Vy * (time.time()-self.start_time)
                self.newAx += self.Vx
                self.newAy += self.Vy
            elif self.back == True:
                self.newAx -= self.Vx
                self.newAy -= self.Vy
            #4 kvadranta lej
            if self.Ax < self.Bx   and self.Ay > self.By :
                if self.newAx >= self.Bx and self.newAy <= self.By and self.start == True: # y preteju prieks si
                    print("start of road, moving forwords")
                    self.start = False
                    self.back = True
                elif self.newAx <= self.Ax and self.newAy >= self.Ay and self.start == False:
                    print("end of road, moving backwords")
                    self.start = True
                    self.back = False
            #1 kvadrants
            elif self.Ax < self.Bx  and self.Ay < self.By:
                if self.newAx >= self.Bx and self.newAy >= self.By and self.start == True: # y preteju prieks si
                    print("start of road, moving forwords")
                    self.start = False
                    self.back = True
                elif self.newAx <= self.Ax and self.newAy <= self.Ay and self.start == False:
                    print("end of road, moving backwords")
                    self.start = True
                    self.back = False
            #3kvadrants
            elif self.Ax > self.Bx  and self.Ay > self.By:
                if self.newAx <= self.Bx and self.newAy <= self.By and self.start == True: # y preteju prieks si
                    print("start of road, moving forwords")
                    self.start = False
                    self.back = True
                elif self.newAx >= self.Ax and self.newAy >= self.Ay and self.start == False:
                    print("end of road, moving backwords")
                    self.start = True
                    self.back = False
            #2 kvadrants
            elif self.Ax > self.Bx  and self.Ay < self.By:
                if self.newAx <= self.Bx and self.newAy >= self.By and self.start == True: # y preteju prieks si
                    print("start of road, moving forwords")
                    self.start = False
                    self.back = True
                elif self.newAx >= self.Ax and self.newAy <= self.Ay and self.start == False:
                    print("end of road, moving backwords")
                    self.start = True
                    self.back = False
            self.calc_distance(self.Ox,self.Oy,self.newAx,self.newAy)
            self.K = self._calc_K()
            self.pl = 10*self.K*(math.log10(self.d))+10*self.K*(math.log10(self.fc))+92.45#gigaherz and kilometeres
            print("The loss is %.2f dB" % self.pl)
            time.sleep(1)
        else:
            raise RuntimeError("Linear mode not initialised")
        return self.pl
            
    def elip_moving(self):
        """
        Calculates the "Free space loss" for eliptical movement of the reciever antenna
        Returns
        -------
        pl : float
            path loss db value "pl".
        """
        if self.circ_mode == True:
            self.Ex=self.Ex+self.Bx*self.v*math.cos(self.angle+(math.pi/2))
            self.Ey=self.Ey+self.By*self.v*math.sin(self.angle+(math.pi/2))
            self.calc_distance(self.Ox,self.Oy,self.Ex,self.Ey)
            self.K = self._calc_K()
            self.pl = 10*self.K*(math.log10(self.d))+10*self.K*(math.log10(self.fc))+92.45#gigaherz and kilometeres
            print("The loss is %.2f dB" % self.pl)
            self.angle += self.v
            time.sleep(1)
        else: 
            raise RuntimeError("Circular mode not initialised")
        return self.pl
            
    def teleport(self, maxdist,sleeptime):
        """
        Calculates the "Free space loss" for teleport movement of the reciever antenna
        This calcualtion requires the input of:
        maximum distance for a jump;
        leeptime: time between the next jump
        
        Returns
        -------
        pl : float
            path loss db value "pl".
        """
        if self.tel_mode == True:
            self.Tx = random.randint(-maxdist,maxdist)
            self.Ty = random.randint(-maxdist,maxdist)
            self.calc_distance(self.Ox,self.Oy,self.Tx,self.Ty)
            self.K = self._calc_K()
            self.pl = 10*self.K*(math.log10(self.d))+10*self.K*(math.log10(self.fc*10**9))+92.45#gigaherz and kilometeres
            print("The loss is %.2f dB" % self.pl)
            time.sleep(sleeptime)
        else: 
            raise RuntimeError("Teleport mode not initialised")
        return self.pl
    def reset(self):
        self.__init__(self.P, self.fc,0,0,Ax = 0, Ay = 0,Bx = 0,By = 0,v =  0, mode = "reset")
        plt.clf()
        plt.close('all')
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
    def drawing(self):
        """
        Drawing function to check if the movement simulated is correct
        """
        if self.mode == "linear":
            self.ax = self.newAx
            self.ay = self.newAy
        elif self.mode == "circular":
            self.ax = self.Ex
            self.ay = self.Ey
        elif self.mode == "static":
            self.ax = self.Ax
            self.ay = self.Ay
        elif self.mode == "teleport":
            self.ax = self.Tx
            self.ay = self.Ty
        self.dx.append(self.ax)
        self.dy.append(self.ay)
        plt.show(block=False)
        self.ax1.plot(self.dx, self.dy, '-ok',color='black')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

if __name__ == "__main__":
        
    #a = PathLoss(1000.0, 60, 0,0,Ax = 100, Ay = 100,Bx = 100, By = 500,v = 10,mode = "teleport", envo="open")#nestrada ar negativiem skaitliem
    a = PathLoss(10.0, 10, 0,0,Ax = 0, Ay = 500, mode="static",envo="open")#nestrada ar negativiem skaitliem
    pl = a.static()
    for i in range(0,10):
        #pl = a.lin_moving()
        #pl = a.static()
        #pl = a.teleport(1000,0.5)
        a.drawing()
    #a.reset()
#plt.close('all')
#    a.elip_moving()
    #a.teleport(1000, 1.0)
#a.reset()
