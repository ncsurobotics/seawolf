import cv2
import numpy as np
import math
global GREY, WHITE, RED, BLACK, BLUE, CHROME_BLUE, GREEN, GUI_IMG, WIDTH, HEIGHT
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
#from point (ox,oy) to (x,y)
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
        
        return -math.pi;
