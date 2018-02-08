#GUI for testing seawolf
#to kill program, hit k

import cv2
import numpy as np
import math
import seawolf as sw
import gui_functions
import sys
sys.path.append('../../mission_control')
import sw3

#Components
ROLL = 0
PITCH = 1
YAW = 2
DEPTH = 3
DEPTH_READER = 4
FORWARD = 5
BOW = 6
STERN = 7
PORT = 8
STAR = 9
STRAFET = 10
STRAFEB = 11
PLAY_BUTTON = 12

def initializeValues():
        d.desiredBearing[ROLL] = realToDisplayRadians(math.radians(sw.var.get("RollPID.Heading")))
        d.desiredBearing[PITCH] = realToDisplayRadians(math.radians(sw.var.get("PitchPID.Heading")))
        d.desiredBearing[YAW] = realToDisplayRadians(math.radians(sw.var.get("YawPID.Heading")))
        d.setSlideValueForDepthReadOnlySlider(DEPTH_READER, sw.var.get("Depth"))
        d.setSlideValue(FORWARD, 0)
def setVars():
            d.setSlideValue(BOW, sw.var.get("Bow"))
            d.setSlideValue(STERN, sw.var.get("Stern"))
            d.setSlideValue(PORT, sw.var.get("Port"))
            d.setSlideValue(STAR, sw.var.get("Star"))
            d.setSlideValue(STRAFET, sw.var.get("StrafeT"))
            d.setSlideValue(STRAFEB, sw.var.get("StrafeB"))
            d.setSlideValueForDepthReadOnlySlider(DEPTH_READER, sw.var.get("Depth"))
            #d.setSlideValue(4, d.slideValue(3))#sw.var.get("DepthPID.Heading"))
            #print(d.slide[3])
            #d.slide[4] = d.slide[3]
            #print(str(d.slideValue(4) + 0) + " " + str(d.slideValue(3)))
def mapValTo(p1,a,b,c,d):
        return (p1-a)*(d-c)/(b-a)+c

#is xr and yr on rect from ox,oy with width w and length l
def isOnSlider(xr,yr,ox,oy,w,l):
        if(ox <= xr and xr <= ox+w and oy <= yr and yr <= oy+l):
            return True
        return False

def dist(x1,y1,x2,y2):
    return math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

def displayToRealRadians(r):
        if(r < math.pi/2):
                return math.degrees(r + math.pi/2)
        if(r > math.pi/2):
                return math.degrees(r - 3*math.pi/2)
        return math.degrees(math.pi)

def realToDisplayRadians(r):
        if(r < 0):
                return r + 3*math.pi/2
        if(r > 0):
                return r - math.pi/2
        return -math.pi/2

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
    bb = 60
    BACKGROUND_COLOR = (bb,bb,bb)
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
        self.change = []
        
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
        self.enabled = []
        self.paused = []

        self.toggle = []

        self.num = 0
        
    def move(self,event,x,y,flags,param):
        global mouseX,mouseY
        for i in range(self.num):
            if(self.kind[i] == "PlayButton"):
                    if event == cv2.EVENT_LBUTTONDOWN and not self.follow[i]:
                            mouseX,mouseY = x,y
                            if isOnSlider(mouseX, mouseY, self.X[i],self.Y[i], self.width[i], self.length[i]):
                                    self.follow[i] = True
                                    self.toggle[i] = True#not self.toggle[i]
                                    self.change[i] = 1
                                    
                            
                            
                    if event == cv2.EVENT_LBUTTONUP:
                            self.follow[i] = False
                            self.toggle[i] = False
                            self.change[i] = 1
                            
                            
            if(self.kind[i] == "Slider") and self.enabled[i]:
                
                if event == cv2.EVENT_LBUTTONDOWN:
                    mouseX,mouseY = x,y
                    if(isOnSlider(x,y,self.X[i],self.Y[i],self.width[i],self.length[i])):
                       self.follow[i] = True
                       self.change[i] = 1
               
                if event == cv2.EVENT_LBUTTONUP:
                    if self.follow[i] == True:
                            self.change[i] = 1
                    self.follow[i] = False
                    
            
                if self.follow[i] == True:
                    self.change[i] = 1
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
                       self.change[i] = 1
               
                if event == cv2.EVENT_LBUTTONUP:
                    if self.follow[i] == True:
                            self.change[i] = 1
                    self.follow[i] = False
                    
            
                if self.follow[i] == True:
                    self.desiredBearing[i] = heading(self.X[i],self.Y[i],self.X[i] + (self.X[i] - x) / 2, self.Y[i] - (self.Y[i] - y) / 2)
                    self.change[i] = 1
                #self.draw(self.X[i],self.Y[i],flags,param,i)
            
            
            
            
    def addComp(self, x, y, fo, ki, ti, ra, de, co, dBear, aBear, pa, wi, le, sl, ma, mi, baTy, mapUp, mapDown, enabled, toggle):
        self.X.append(x)
        self.Y.append(y)
        self.follow.append(fo)
        self.kind.append(ki)
        self.title.append(ti)
        self.change.append(0)
        
        self.radius.append(ra)
        self.degree.append(de)
        self.color.append(co)
        self.desiredBearing.append(math.radians(dBear))
        self.actualBearing.append(aBear)
        self.paused.append(pa)

        self.width.append(wi)
        self.length.append(le)
        self.slide.append(sl)
        self.max.append(ma)
        self.min.append(mi)
        self.barType.append(baTy)
        self.mapUp.append(mapUp)
        self.mapDown.append(mapDown)
        self.enabled.append(enabled)

        self.toggle.append(toggle)
        
        self.drawTitle(self.num)
        self.num += 1
                  
    def addDial(self, r, d, c, x, y, t):
        self.addComp(x, y, False, "Dial", t, r, d, c, math.radians(d), 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1)
        
    def addSlider(self, w, l, s, ma, mi, x, y, bt, t, mu, md, en):
        self.addComp(x, y, False, "Slider", t, -1, -1, -1, -1, -1, -1, w, l, s, ma, mi, bt, mu, md, en, -1)
        
    def addPlayButton(self, w, l, x, y, ti, tog):
        self.addComp(x, y, False, "PlayButton", ti, -1, -1, -1, -1, -1, -1, w, l, -1, -1, -1, -1, -1, -1, -1, tog)
        
    def drawAll(self):
        for k in range(self.num):
             #if(self.change[k] == 1):
                     #print self.kind[k]
             self.draw(k)
    def drawTitle(self, i):
            if(self.kind[i] == "Slider"):
                if self.barType[i] == 1:
                        self.textAt(self.X[i] - 25,self.Y[i]-40,self.title[i])
                if self.barType[i] == 0:
                        self.textAt(self.X[i],self.Y[i]-50,self.title[i])
                
            if(self.kind[i] == "Dial"):
                self.textAt(self.X[i]-8*len(self.title[i]),self.Y[i]-105,self.title[i])
            
    def draw(self,i):
        x = self.X[i]
        y = self.Y[i]
        if(self.kind[i] == "PlayButton"):
            if(self.toggle[i] == False):
                    color = (200,200,200)
                    msg = " Pause"
            if(self.toggle[i] == True):
                    color = (0,200,0)
                    msg = "Pausing"
            self.rect(self.X[i] - 8, self.Y[i] - 8, self.width[i] + 16, self.length[i] + 16, grey)
            cv2.rectangle(img, (self.X[i], self.Y[i]), (self.X[i]+self.width[i], self.Y[i]+self.length[i]), color, thickness=-1, lineType=8, shift=0)
            self.textAtC(self.X[i], self.Y[i]+30, msg, (50,50,50))
        if(self.kind[i] == "Dial"):
            #background
            cv2.circle(img,(x,y),int(self.radius[i]*1.3),self.BACKGROUND_COLOR,-1)
            #outer circle main
            cv2.circle(img,(x,y),int(self.radius[i]*1.1),grey,-1)
            #inner circle main
            cv2.circle(img,(x,y),self.radius[i],white,-1)

            #line read
            cv2.line(img,(x,y), ((int(x-self.radius[i]*math.cos(self.actualBearing[i]))),int((y+self.radius[i]*math.sin(self.actualBearing[i])))), (0,0,255), thickness = 4, lineType = 8, shift = 0)   
            
            #line write
            cv2.line(img,(x,y), ((int(x-self.radius[i]*math.cos(self.desiredBearing[i]))),int((y+self.radius[i]*math.sin(self.desiredBearing[i])))), dark, thickness = 4, lineType = 8, shift = 0)        
            #outer circle small
            cv2.circle(img,((int(x-self.radius[i]*math.cos(self.desiredBearing[i]))),int((y+self.radius[i]*math.sin(self.desiredBearing[i])))),self.radius[i]/4,dark,-1)
            #inner circle small
            cv2.circle(img,((int(x-self.radius[i]*math.cos(self.desiredBearing[i]))),int((y+self.radius[i]*math.sin(self.desiredBearing[i])))),self.radius[i]/6,white,-1)
            #clear text
            cv2.rectangle(img, (self.X[i]+textDx-50, self.Y[i]-self.radius[i]+textDy-30), (self.X[i]+150-50, self.Y[i]-self.radius[i]+textDy+10), self.BACKGROUND_COLOR, thickness=-1, lineType=8, shift=0)        
            #text write
            cv2.putText(img, str(toRealDegrees(int(round(math.degrees(self.desiredBearing[i]),0)))), (self.X[i]+textDx-50, self.Y[i]-self.radius[i]+textDy), font, 0.8, (255, 255, 255), 1, 8)
            #text read
            cv2.putText(img, str(toRealDegrees(int(round(math.degrees(self.actualBearing[i]),0)))), (self.X[i]+textDx+100-50, self.Y[i]-self.radius[i]+textDy), font, 0.8, (0, 0, 255), 1, 8)
            #clear text paused
            cv2.rectangle(img, (self.X[i]+8*len(self.title[i]), self.Y[i]-125), (self.X[i]+8*len(self.title[i])+50, self.Y[i]-100), self.BACKGROUND_COLOR, thickness=-1, lineType=8, shift=0)  
            #text paused
            self.textAt(self.X[i]+8*len(self.title[i]),self.Y[i]-105,str(self.paused[i]))
        if(self.kind[i] == "Slider"):
            #background
            if self.enabled[i]:
                    cv2.rectangle(img, (self.X[i]-10, self.Y[i]-10), (self.X[i]+self.width[i]+10, self.Y[i]+self.length[i]+10), self.BACKGROUND_COLOR, thickness=-1, lineType=8, shift=0)
            #outer mid rect
            if self.enabled[i]:
                    cv2.rectangle(img, (self.X[i], self.Y[i]), (self.X[i]+self.width[i], self.Y[i]+self.length[i]), grey, thickness=-1, lineType=8, shift=0)   
            #inner mid rect
            if self.enabled[i]:
                    cv2.rectangle(img, (self.X[i]+5, self.Y[i]+5), (self.X[i]+self.width[i]-5, self.Y[i]+self.length[i]-5), white, thickness=-1, lineType=8, shift=0)

            
            #slider
                #outer
            sliding_bar_color = (0,0,255)
            if self.enabled[i]:
                  sliding_bar_color = (200,200,200)  
            if self.barType[i] == 0: #horiz
                   cv2.rectangle(img, (self.X[i]+self.slide[i]-10/2, self.Y[i]), (self.X[i]+self.slide[i]+10-10/2, self.Y[i]+self.length[i]), sliding_bar_color, thickness=-1, lineType=8, shift=0)
            if self.barType[i] == 1:#vertical
                    cv2.rectangle(img, (self.X[i], self.Y[i]+self.slide[i]-10/2), (self.X[i]+self.width[i], self.Y[i]+self.slide[i]+10-10/2), sliding_bar_color, thickness=-1, lineType=8, shift=0)

             
                #inner
            
            #clear text
            if self.enabled[i]:
                    if self.barType[i] == 1:
                            cv2.rectangle(img, (self.X[i] - 70, self.Y[i]-30), (self.X[i]+20, self.Y[i]-5), self.BACKGROUND_COLOR, thickness=-1, lineType=8, shift=0)
                    if self.barType[i] == 0:
                            cv2.rectangle(img, (self.X[i], self.Y[i]-40), (self.X[i]+90, self.Y[i]-10), self.BACKGROUND_COLOR, thickness=-1, lineType=8, shift=0)  
            #text
            if self.enabled[i]:
                    if self.barType[i] == 1:
                            cv2.putText(img, ("%.2f" % (self.slideValue(i))), (self.X[i] - 70, self.Y[i]-10), font, 0.8, (255, 255, 255), 1, 8)
                    if self.barType[i] == 0:
                            cv2.putText(img, ("%.2f" % (self.slideValue(i))), (self.X[i], self.Y[i]-20), font, 0.8, (255, 255, 255), 1, 8)
            
    def rect(self, x, y, w, h, col):
            cv2.rectangle(img, (x, y), (x+w, y+h), col, thickness=-1, lineType=8, shift=0)
    def writeHub(self, hubVar, guiVar, i):
            if self.change[i] == 1:
                    if guiVar == "realRadDesBear":
                            sw.var.set(hubVar, float(displayToRealRadians(d.desiredBearing[i])))
                            self.change[i] = 0
                    if guiVar == "slideValue":
                            sw.var.set(hubVar, float(d.slideValue(i)))
                            self.change[i] = 0
                    return True 
            return False
            
    def textAtC(self,x,y,text, col):
        cv2.putText(img, text, (x, y), font, 0.8, col, 1, 8)
    def textAt(self,x,y,text):
        cv2.putText(img, text, (x, y), font, 0.8, (255, 255, 255), 1, 8)
    def setSlideValue(self, i, val):
            if self.mapDown[i] - self.mapDown[i]*.1 >= val and val >= self.mapUp[i] * 1.1:
                    if self.barType[i] == 1:#vertical
                            self.slide[i] = int(round((-(self.length[i]/(self.mapDown[i] - self.mapUp[i])) * (val - self.mapUp[i])) + self.length[i],0))
                    if self.barType[i] == 0:#horiz
                            self.slide[i] = int(round(((self.width[i]/(self.mapDown[i] - self.mapUp[i])) * (val - self.mapUp[i])),0))
    def setSlideValueForDepthReadOnlySlider(self, i, val):
            #bad value
            if (-3.0 <= val and val <= 0.5) == False:
                    return 
            #real value
            self.slide[i] = int(round(-42.9 * (val + 3) + 150, 0))
    #Given the cartesian position along the slider, return the scaled value from max and min
    def slideValue(self,i):
        if self.barType[i] == 0: #horiz
                return mapValTo(self.slide[i], 0, self.width[i], self.mapUp[i], self.mapDown[i])
        if self.barType[i] == 1: #vertical
                return mapValTo(self.slide[i], self.length[i], 0, self.mapUp[i], self.mapDown[i])
################################################################################################################################################################start of main
seawolfIsRunning = True
delay = 5
             
if(seawolfIsRunning):
        sw.loadConfig("../../conf/seawolf.conf")
        sw.init("GUI") 
WIDTH = 500
HEIGHT = 1000
img = np.zeros((HEIGHT,WIDTH,3), np.uint8)
cv2.namedWindow('image')

d = Controller()
cv2.rectangle(img, (0, 0), (WIDTH, HEIGHT), d.BACKGROUND_COLOR, thickness=-1, lineType=8, shift=0)
up = 1.0
down = -1.0

#don't change the order of these
d.addDial(50,30,(0,0,255), 100, 460, "Roll")
d.addDial(50,30,(0,0,255), 300, 460, "Pitch")
d.addDial(50,30,(0,0,255), 100, 650, "Yaw")

d.addSlider(20, 150, 50, 100, 50, 290, 590, 1, "Depth", -3, .5, True)
d.addSlider(20, 150, 50, 100, 50, 300, 590, 1, "", -3, .5, False) #actual depth
d.addSlider(150, 20, 50, 100, 50, 40, 800, 0, "Forward", down, up, True)


d.addSlider(150, 20, 50, 100, 50, 40, 100, 0, "Bow", down, up, True)
d.addSlider(150, 20, 50, 100, 50, 240, 100, 0, "Stern", down, up, True)
d.addSlider(150, 20, 50, 100, 50, 40, 200, 0, "Port", down, up, True)
d.addSlider(150, 20, 50, 100, 50, 240, 200, 0, "Star", down, up, True)
d.addSlider(150, 20, 50, 100, 50, 40, 300, 0, "Strafet", down, up, True)
d.addSlider(150, 20, 50, 100, 50, 240, 300, 0, "Strafeb", down, up, True)


d.addPlayButton(100, 100, 250, 800, "Play Button", False)

cv2.setMouseCallback('image',d.move)

count = 0

initializeValues()
while(1):
    cv2.imshow('image',img)
    d.drawAll()
    k = cv2.waitKey(20) & 0xFF
    count += 1
    if count >= delay:
            count = 0
    

    if(seawolfIsRunning and count == 0):
            #setting values in seawolf to change
                    #thruster sliders
            d.writeHub("Bow", "slideValue", BOW)
            d.writeHub("Stern", "slideValue", STERN)
            d.writeHub("Port", "slideValue", PORT)
            d.writeHub("Star", "slideValue", STAR)
            d.writeHub("StrafeT", "slideValue", STRAFET)
            d.writeHub("StrafeB", "slideValue", STRAFEB)
            d.writeHub("DepthPID.Heading", "slideValue", 3)
            
                    #dials
            if d.change[5]:
                    a = sw3.Forward(d.slideValue(5))
                    a.start()
                    if abs(d.slideValue(5)) < 0.01:
                            a.cancel()
                    d.change[5] = 0
            if(d.writeHub("RollPID.Heading", "realRadDesBear", ROLL)):
                    d.setSlideValue(BOW, sw.var.get("Bow"))
                    d.setSlideValue(STERN, sw.var.get("Stern"))
                    d.setSlideValue(PORT, sw.var.get("Port"))
                    d.setSlideValue(STAR, sw.var.get("Star"))
                    d.setSlideValue(STRAFET, sw.var.get("StrafeT"))
                    d.setSlideValue(STRAFEB, sw.var.get("StrafeB"))
            
            #d.writeHub("PitchPID.Heading", "realRadDesBear", 1)#overwrite bow and stern then move sliders
            if(d.writeHub("PitchPID.Heading", "realRadDesBear", 1)):
                    d.setSlideValue(BOW, sw.var.get("Bow"))
                    d.setSlideValue(STERN, sw.var.get("Stern"))
                    d.setSlideValue(PORT, sw.var.get("Port"))
                    d.setSlideValue(STAR, sw.var.get("Star"))
                    d.setSlideValue(STRAFET, sw.var.get("StrafeT"))
                    d.setSlideValue(STRAFEB, sw.var.get("StrafeB"))
                    
            
            #do this move sliders for bow [6] and stern [7]. self.slide[6,7] = mapval to inverse of typical. map value to x value . need inverse function. value to global x,y given mapping vals and global coordinates
            if(d.writeHub("YawPID.Heading", "realRadDesBear", 2)):
                    d.setSlideValue(BOW, sw.var.get("Bow"))
                    d.setSlideValue(STERN, sw.var.get("Stern"))
                    d.setSlideValue(PORT, sw.var.get("Port"))
                    d.setSlideValue(STAR, sw.var.get("Star"))
                    d.setSlideValue(STRAFET, sw.var.get("StrafeT"))
                    d.setSlideValue(STRAFEB, sw.var.get("StrafeB"))

            #changing values in gui read from seawolf
            
            d.actualBearing[ROLL] = realToDisplayRadians(math.radians(sw.var.get("SEA.Roll")))#change these to better degree converter where math.radians() is
            d.actualBearing[PITCH] = realToDisplayRadians(math.radians(sw.var.get("SEA.Pitch")))
            d.actualBearing[YAW] = realToDisplayRadians(math.radians(sw.var.get("SEA.Yaw")))
            #d.actualBearing[0] = realToDisplayRadians(math.radians(0))#change these to better degree converter where math.radians() is
            #d.actualBearing[1] = realToDisplayRadians(math.radians(0))
            #d.actualBearing[2] = realToDisplayRadians(math.radians(0))
            d.paused[ROLL] = sw.var.get("RollPID.Paused")
            d.paused[PITCH] = sw.var.get("PitchPID.Paused")
            d.paused[YAW] = sw.var.get("YawPID.Paused")
            d.paused[DEPTH] = sw.var.get("DepthPID.Paused")
            
            setVars()
            #print actual depth in red
            d.rect(330,555,80,30,d.BACKGROUND_COLOR)
            d.textAtC(330,580, str(round(sw.var.get("Depth"),2)), (0,0,255))
            if d.change[12] == 1:
                    d.change[12] = 0
                    if d.toggle[12] == True:
                            sw3.ZeroThrusters().start()
                            d.setSlideValue(DEPTH, 0)
                            d.setSlideValue(FORWARD, 0)
                            a = sw3.Forward(d.slideValue(5))
                            a.start()
                            d.setSlideValue(BOW, sw.var.get("Bow"))
                            d.setSlideValue(STERN, sw.var.get("Stern"))
                            d.setSlideValue(PORT, sw.var.get("Port"))
                            d.setSlideValue(STAR, sw.var.get("Star"))
                            d.setSlideValue(STRAFET, sw.var.get("StrafeT"))
                            d.setSlideValue(STRAFEB, sw.var.get("StrafeB"))
 
    if k == 107: #hit k for kill
        sw.close()
        cv2.destroyWindow('image')
        break
    elif k == ord('a'):
        print mouseX,mouseY
