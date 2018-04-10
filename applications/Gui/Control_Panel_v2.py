"""
GUI for controlling seawolf for testing.
"""

import cv2
from gui_graphics import *
from gui_gui import *
from gui_component import *
from gui_textbox import *
from gui_dial import *
from gui_slider import *
import numpy as np
import math
import seawolf as sw
import gui_functions
import sys
sys.path.append('../../mission_control')
import sw3

#from abc import ABC, abstractmethod
import abc

#global variables
global GUI_IMG




"""
Maps the value given on an input range to a scaled value on an output range. For instance, given the point 1 on the input scale 0 to 5,
you would want to set this to 2 on the output scale 0 to 10. This function takes parameters for the input point, input scale start, input
scale end, output scale start, and output scale end, and returns the matching point to the input point, but on the output scale.

p1 - point on input scale to be mapped
a - start of the input range
b - end of the input range
c - start of the output range
d - end of the output range
return input point scaled to output range
"""
def mapValTo(p1,a,b,c,d):
        return (p1-a)*(d-c)/(b-a)+c

"""
class HorizontalSlider(Slider):
class PlayButton(Component):
class Text(Component):
"""

def main():
    seawolfIsRunning = True
    if(seawolfIsRunning):
        sw.loadConfig("../../conf/seawolf.conf")
        sw.init("GUI")
    
    #GUI_IMG = np.zeros((HEIGHT,WIDTH,3), np.uint8)
    cv2.namedWindow('Control Panel')
    g = GUI()
    down = -1.0
    up = 1.0
    g.addComponent(VerticalSlider(290, 590, 20, 150, -3, .5, "Depth"))
    g.addComponent(HorizontalSlider(40, 800, 150, 20, down, up, "Forward"))

    g.addComponent(Dial(100, 460, "Roll"))
    g.addComponent(Dial(300, 460, "Pitch"))
    g.addComponent(Dial(100, 650, "Yaw"))

    g.addComponent(HorizontalSlider(40, 100, 150, 20, down, up, "Bow"))
    g.addComponent(HorizontalSlider(240, 100, 150, 20, down, up, "Stern"))
    g.addComponent(HorizontalSlider(40, 200, 150, 20, down, up, "Port"))
    g.addComponent(HorizontalSlider(240, 200, 150, 20, down, up, "Star"))
    g.addComponent(HorizontalSlider(40, 300, 150, 20, down, up, "Strafet"))
    g.addComponent(HorizontalSlider(240, 300, 150, 20, down, up, "Strafeb"))
    
    
   # g.addComponent()
   
    
    cv2.setMouseCallback('Control Panel',g.handleMouseEvent)
    while(True):
        rect(0, 0, WIDTH, HEIGHT, BLACK)
        g.drawComponents()
        cv2.imshow('Control Panel',GUI_IMG)
        k = cv2.waitKey(20) & 0xFF
        #if key is numeric or modifies number, modify number in selected text box
        if (ord('0') <= k and k <= ord('9')) or k == BACKSPACE or k == ord('\n') or k == ord('.') or k == ord('-'):
            g.modifySelectedTextBox(k)
        if k == 107 or k == 27 or cv2.getWindowProperty('Control Panel',1) < 1: 
            sw.close()
            cv2.destroyWindow('Control Panel')
            break
main()