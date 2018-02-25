"""
GUI for controlling seawolf for testing.
"""

import cv2
import numpy as np
import math
import seawolf as sw
import gui_functions
import sys
sys.path.append('../../mission_control')
import sw3

#from abc import ABC, abstractmethod
import abc
#Helpful functions
def circle(x, y, r, color, img):
    pass
def rect(x, y, w, l, color, img):
    pass
def line(x1, y1, x2, y2, thickness, color, img):
    cv2.line(img, (x1,y1), (x2,y2), color, thickness = 4, lineType = 8, shift = 0)
    pass
def textAt(x, y, text, color, size, img):
    pass
#global variables
global GREY, WHITE, RED
GREY = (140,140,140)
WHITE = (255,255,255)
RED = (0, 0, 255) #RGB is read backwards in opencv
"""
class AbstractClassExample(ABC):
 
    def __init__(self, value):
        self.value = value
        super().__init__()
    
    @abstractmethod
    def do_something(self):
        pass
"""

class GUI:
    #global BACKGROUND_COLOR
    BACKGROUND_COLOR = (0,0,0)
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
    def __init__(self):
        self.components = []
        self.components.append(Dial(150,150, "Roll"))
        self.components.append(Dial(150,300, "Pitch"))
        #append all components
        pass
    def handleMouseEvent(self, event, x, y, flags, param):
        #go througgh each component and handle it just in case
        for comp in self.components:
            comp.handleMouseEvent(x,y,event)
        #print( str(x) + ", " + str(y) )
        #print(event)
        pass
    def drawComponents(self):
        #for each component in components, component.draw()
        pass
class Component:
    def __init__(self, x, y, title):
        self.x = x
        self.y = y
        self.title = title
        self.change = False
    
    #@abstractmethod
    def handleMouseEvent(self, x, y):
        pass
    #@abstractmethod
    def draw(self):
        pass
    def move(self, x, y):
        pass
class Dial(Component):
    def __init__(self, x, y, title):
        self.radius = 60
        self.degree = 0
        self.desiredBearing = 0
        self.actualBearing = 0
        self.following = False
        self.title = title
        self.paused = False
        Component.__init__(self, x, y, title)
    def handleMouseEvent(self, x, y, event):
        print(self.title)
    def draw():
        pass
    #move desired bearing toward (x,y), using special 180 and -180 scale
    def move(self, x, y):
        pass
    def moveReadIndicator(self, degrees):
        pass
        

class  Slider(Component):
    def __init__(self, x, y, width, length, min, max, title):
        self.width = width
        self.length = length
        self.min = min
        self.max = max
        self.ti
        Component.__init__(self, x, y, title)
    

class VerticalSlider(Slider):
    def __init__(self, x, y, width, length, min, max, title):
        Slider.__init__(self, x, y, width, length, min, max, title)
    #move slider horizontally
    def move(self, x, y):
        pass
    
"""
class HorizontalSlider(Slider):
class PlayButton(Component):
class Text(Component):
"""

def main():
    WIDTH = 500
    HEIGHT = 1000
    img = np.zeros((HEIGHT,WIDTH,3), np.uint8)
    cv2.namedWindow('Control Panel')

    g = GUI()
    cv2.rectangle(img, (0, 0), (WIDTH, HEIGHT), g.BACKGROUND_COLOR, thickness=-1, lineType=8, shift=0)
    cv2.setMouseCallback('Control Panel',g.handleMouseEvent)
    while(True):
        cv2.imshow('Control Panel',img)
        g.drawComponents()
        k = cv2.waitKey(20) & 0xFF
        if k == 107 or k == 27 or cv2.getWindowProperty('Control Panel',1) < 1: 
            cv2.destroyWindow('Control Panel')
            break
main()