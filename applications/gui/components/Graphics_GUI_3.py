"""
Collection of drawing functions.
Wrappers of opencv drawing functions to reduce boiler plate code.
"""

import cv2
import numpy as np
import math
WIDTH = 500
HEIGHT = 1000
GUI_IMG = np.zeros((HEIGHT,WIDTH,3), np.uint8)

#RGB is read backwards in opencv
BLACK = (0,0,0)
GREY = (140,140,140)
WHITE = (255,255,255)
CHROME_BLUE = (245,140,76)
BLUE = (255,0,0)
RED = (0, 0, 255) 
GREEN = (0, 255, 0)
DARK = (32,54,76)
LIGHT_GREY = (200, 200, 200)
DARK_GREY = (50, 50, 50)
BACKGROUND_COLOR = DARK_GREY


#Helpful functions
def circle(x, y, radius, color):
    cv2.circle(GUI_IMG, (x,y), radius, color, -1)
    pass

def rect(x, y, w, l, color):
    cv2.rectangle(GUI_IMG, (int(x), int(y)), (int(x + w), int(y + l)), color, thickness=-1, lineType=8, shift=0)

def line(x1, y1, x2, y2, thickness, color):
    cv2.line(GUI_IMG, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness = 4, lineType = 8, shift = 0)
    pass

def textAt(x, y, text, color):
    cv2.putText(GUI_IMG, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, 8)
    pass

#point (x,y) in circle
def isInCircle(circleX, circleY, circleRadius, x, y):
    deltaX = circleX - x
    deltaY = circleY - y
    return math.sqrt( deltaX * deltaX + deltaY * deltaY ) <= circleRadius

#point (x,y) in rectangle
def isInRect(rectX, rectY, rectWidth, rectLength, x, y):
    return rectX <= x and x <= rectX + rectWidth and rectY <= y and y <= rectY + rectLength

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
