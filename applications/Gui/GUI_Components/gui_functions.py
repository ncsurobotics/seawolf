import cv2
import numpy as np
import math
#import seawolf as sw
import sys

def mapValTo(p1,a,b,c,d):
        return (p1-a)*(d-c)/(b-a)+c


def isOnSlider(xr,yr,ox,oy,w,l):
        if(ox <= xr and xr <= ox+w and oy <= yr and yr <= oy+l):
            return True
        return False

def dist(x1,y1,x2,y2):
    return math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

def displayToRealRadians(r):
        if(r < math.pi/2):
                return r + math.pi/2
        if(r > math.pi/2):
                return r - 3*math.pi/2
        return math.pi

def realToDisplayRadians(r):
        if(r < 0):
                return r + 3*math.pi/2
        if(r > 0):
                return r - math.pi/2
        return math.pi/2

def inverseDegreesToRadians(d):
    d += math.pi/2
    #if d>=-math.pi/2 and d<=math.pi/2:
        #d += math.pi/2
    if d>math.pi:
        d -= math.pi
    #d += 90
    return math.radians(d)

    #return toRealDegrees(math.radians(d))

def toRealDegrees(d):
    d -= 90
    if d < 0:
        return d + 180
    if d >= 0:
        return d-180
    return 0
    #flip
  #  if d >= 90 and d <= 270:
   #     return d-90
    #if d >= -90 and d < 90:
     #   return d

def heading(ox,oy,x,y):
        if(ox<x and oy<y):
            return math.pi-math.pi/2-math.atan2(x-ox,y-oy)
        if(x<ox and oy<y):
            return math.pi-math.pi/2-math.atan2(x-ox,y-oy)

        if(ox<x and y<oy):
            return math.pi-math.pi/2-math.atan2(x-ox,y-oy)
        if(x<ox and y<oy):
            return math.pi-math.pi/2-math.atan2(x-ox,y-oy)

        if(x==ox and y < oy):
            return math.pi+math.pi/2
        if(x==ox and y > oy):
            return math.pi/2
        if(x<ox and y == oy):
            return math.pi
        if(x>ox and y == oy):
            return 0
        
        return -3.14;
################################################################    Controller
class Controller:
    global PI, dark, light, grey, white, FONT_HERSHEY_SIMPLEX, font, textDx, textDy
    PI = 3.1459
    dark = (32,54,76)
    light = (0,51,102)
    white = (255,255,255)
    grey = (140,140,140)
    FONT_HERSHEY_SIMPLEX = 0,
    font = cv2.FONT_HERSHEY_SIMPLEX
    textDx = -25
    textDy = -20
    def __init__(self):

        self.X = []
        self.Y = []
        self.follow = []
        self.kind = []
        self.title = []
        
        self.width = []
        self.length = []
        self.slide = []
        self.max = []
        self.min = []
        self.barType = []

        self.radius = []
        self.degree = []
        self.color = []
        self.desiredBearing = []
        self.dialNum = 0
        self.actualBearing = []
        self.mapUp = []
        self.mapDown = []

        self.num = 0
        
    def move(self,event,x,y,flags,param):
        global mouseX,mouseY
        for i in range(self.num):
            
            if(self.kind[i] == "Slider"):
                
                if event == cv2.EVENT_LBUTTONDOWN:
                    mouseX,mouseY = x,y
                    if(isOnSlider(x,y,self.X[i],self.Y[i],self.width[i],self.length[i])):
                       self.follow[i] = True
               
                if event == cv2.EVENT_LBUTTONUP:
                    self.follow[i] = False
            
                if self.follow[i] == True:
                    if self.barType[i] == 0: #horiz
                            if(x>=self.X[i] and x <= self.X[i]+self.width[i]):
                                self.slide[i] = x-self.X[i]
                    if self.barType[i] == 1: #vertical
                            if(y>=self.Y[i] and y <= self.Y[i]+self.length[i]):
                                self.slide[i] = y-self.Y[i]
                
                #self.draw(self.X[i],self.Y[i],flags,param,i)


                
            if(self.kind[i] == "Dial"):
                if event == cv2.EVENT_LBUTTONDOWN:
                    mouseX,mouseY = x,y
                    if(dist(self.X[i],self.Y[i],x,y) <= self.radius[i]*1.4):
                       self.follow[i] = True
               
                if event == cv2.EVENT_LBUTTONUP:
                    self.follow[i] = False
            
                if self.follow[i] == True:
                    self.desiredBearing[i] = heading(self.X[i],self.Y[i],x,y)
                #self.draw(self.X[i],self.Y[i],flags,param,i)
            
            
            
            
            
    def addDial(self, r, d, c, x, y, t):
        
        self.X.append(x)
        self.Y.append(y)
        self.follow.append(False)
        self.kind.append("Dial")
        self.title.append(t)
        self.drawTitle(self.num)
        
        self.radius.append(r)
        self.degree.append(d)
        self.color.append(c)
        self.desiredBearing.append(math.radians(d))
        self.actualBearing.append(0)

        self.width.append(-1)
        self.length.append(-1)
        self.slide.append(-1)
        self.max.append(-1)
        self.min.append(-1)
        self.barType.append(-1)
        self.mapUp.append(-1)
        self.mapDown.append(-1)

        self.num += 1
        
    def addSlider(self, w, l, s, ma, mi, x, y, bt, t, mu, md):
        self.X.append(x)
        self.Y.append(y)
        self.follow.append(False)
        self.kind.append("Slider")
        self.title.append(t)
        self.drawTitle(self.num)
        
        self.radius.append(-1)
        self.degree.append(-1)
        self.color.append(-1)
        self.desiredBearing.append(-1)
        self.actualBearing.append(-1)

        self.width.append(w)
        self.length.append(l)
        self.slide.append(s)
        self.max.append(ma)
        self.min.append(mi)
        self.barType.append(bt)
        self.mapUp.append(mu)
        self.mapDown.append(md)

        self.num += 1
        
    def drawAll(self):
        for k in range(self.num):
             self.draw(k)
    def drawTitle(self, i):
            if(self.kind[i] == "Slider"):
                self.textAt(self.X[i],self.Y[i]-50,self.title[i])
            if(self.kind[i] == "Dial"):
                self.textAt(self.X[i]-8*len(self.title[i]),self.Y[i]-105,self.title[i])
            
    def draw(self,i):
        x = self.X[i]
        y = self.Y[i]
        if(self.kind[i] == "Dial"):
            #background
            cv2.circle(img,(x,y),int(self.radius[i]*1.3),(0,0,0),-1)
            #outer circle main
            cv2.circle(img,(x,y),int(self.radius[i]*1.1),grey,-1)
            #inner circle main
            cv2.circle(img,(x,y),self.radius[i],white,-1)

            #line read
            cv2.line(img,(x,y), ((int(x+self.radius[i]*math.cos(self.actualBearing[i]))),int((y+self.radius[i]*math.sin(self.actualBearing[i])))), (0,0,255), thickness = 4, lineType = 8, shift = 0)   
            
            #line write
            cv2.line(img,(x,y), ((int(x+self.radius[i]*math.cos(self.desiredBearing[i]))),int((y+self.radius[i]*math.sin(self.desiredBearing[i])))), dark, thickness = 4, lineType = 8, shift = 0)        
            #outer circle small
            cv2.circle(img,((int(x+self.radius[i]*math.cos(self.desiredBearing[i]))),int((y+self.radius[i]*math.sin(self.desiredBearing[i])))),self.radius[i]/4,dark,-1)
            #inner circle small
            cv2.circle(img,((int(x+self.radius[i]*math.cos(self.desiredBearing[i]))),int((y+self.radius[i]*math.sin(self.desiredBearing[i])))),self.radius[i]/6,white,-1)
            #clear text
            cv2.rectangle(img, (self.X[i]+textDx-50, self.Y[i]-self.radius[i]+textDy-30), (self.X[i]+150-50, self.Y[i]-self.radius[i]+textDy+10), (0,0,0), thickness=-1, lineType=8, shift=0)        
            #text write
            cv2.putText(img, str(toRealDegrees(int(math.degrees(self.desiredBearing[i])))), (self.X[i]+textDx-50, self.Y[i]-self.radius[i]+textDy), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
            #text read
            cv2.putText(img, str(toRealDegrees(int(math.degrees(self.actualBearing[i])))), (self.X[i]+textDx+100-50, self.Y[i]-self.radius[i]+textDy), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        if(self.kind[i] == "Slider"):
            #background
            cv2.rectangle(img, (self.X[i]-10, self.Y[i]-10), (self.X[i]+self.width[i]+10, self.Y[i]+self.length[i]+10), (0,0,0), thickness=-1, lineType=8, shift=0)
            #outer mid rect
            cv2.rectangle(img, (self.X[i], self.Y[i]), (self.X[i]+self.width[i], self.Y[i]+self.length[i]), dark, thickness=-1, lineType=8, shift=0)   
            #inner mid rect
            cv2.rectangle(img, (self.X[i]+5, self.Y[i]+5), (self.X[i]+self.width[i]-5, self.Y[i]+self.length[i]-5), white, thickness=-1, lineType=8, shift=0)

            
            #slider
                #outer
            if self.barType[i] == 0: #horiz
                   cv2.rectangle(img, (self.X[i]+self.slide[i]-10/2, self.Y[i]), (self.X[i]+self.slide[i]+10-10/2, self.Y[i]+self.length[i]), (200,200,200), thickness=-1, lineType=8, shift=0)
            if self.barType[i] == 1:#vertical
                    cv2.rectangle(img, (self.X[i], self.Y[i]+self.slide[i]-10/2), (self.X[i]+self.width[i], self.Y[i]+self.slide[i]+10-10/2), (200,200,200), thickness=-1, lineType=8, shift=0)

             
                #inner
            
            #clear text
            cv2.rectangle(img, (self.X[i], self.Y[i]-40), (self.X[i]+90, self.Y[i]-10), (0,0,0), thickness=-1, lineType=8, shift=0)        
            #text
            cv2.putText(img, ("%.2f" % (self.slideValue(i))), (self.X[i], self.Y[i]-20), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
            #cv2.rectangle(img, (self.X[i], self.Y[i]), (self.X[i]+self.width[i], self.Y[i]+self.length[i]), (0,255,0), thickness=-1, lineType=8, shift=0)
    def textAt(self,x,y,text):
        cv2.putText(img, text, (x, y), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
    def slideValue(self,i):
        #return (slope)*(self.slide[i]-
        #return self.slide[i]
        #return ((self.slide[i]-self.X[i])/self.width[i])+self.min[i]#add max line formula
        if self.barType[i] == 0: #horiz
                return mapValTo(self.slide[i], 0, self.width[i], self.mapUp[i], self.mapDown[i])
        if self.barType[i] == 1: #vertical
                return mapValTo(self.slide[i], self.length[i], 0, self.mapUp[i], self.mapDown[i])

