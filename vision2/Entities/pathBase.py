import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from VisObj import visObjects


visObj = "path"
obj = visObjects[visObj]
keys = obj([False, 0, 0, 0]).keys

def ProcessFrame(frame):
  out = obj([False, 0, 0, 0])
  pRed = frame[:, :, 2]
  frame = norm(frame)
  red = frame[:,:,2]
  debugFrame("red", red)
  (row, col, pages) = frame.shape
  maxArea = (row * col)/3
  minArea = 200
  red = cv2.medianBlur(red, ksize = 3)
  ret, thresh = cv2.threshold(red, 120, 255, cv2.THRESH_BINARY)
  debugFrame("threshOg", thresh)
  kernel = np.ones((7,7),np.uint8)
  thresh = cv2.erode(thresh,kernel, iterations = 2)
  debugFrame("thresh", thresh)
  contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  possiblePoles = []
  if contours != None:
    for cont in contours:
      if len(cont) < 3:
        continue;
      (center, (w, h), ang) = cv2.minAreaRect(cont)
      area = w * h
      aspectRatio = 0
      if w != 0:
        aspectRatio = h / w
      if aspectRatio < 1 and aspectRatio != 0:
      	aspectRatio = 1/aspectRatio
      
      
      if area > 1000 and aspectRatio > 3 and aspectRatio < 13:
        angp = abs(ang)
        angp = abs(angp - round((angp/90.0)) * 90)
        loc = (int(center[0]), int(center[1]))
        cv2.drawContours(frame, [cont], -1, (0,0, 0), 3)
        [vx,vy,x,y] = cv2.fitLine(cont, 2,0,0.01,0.01)
        if vx  > .01:
          lefty = int((-x*vy/vx) + y) 
          righty = int(((col-x)*vy/vx)+y) 
          cv2.line(frame,(col-1,righty),(0,lefty),(0,255,0),2)
        angm = math.degrees(math.atan2(vy,vx))
        angM = angm - round((angm/90.0)) * 90
        stringOut = "angP %.2f, asp %.2f" % (angM, aspectRatio)
        cv2.putText(frame, stringOut, loc, cv2.FONT_HERSHEY_SIMPLEX, .5, 255)
        out = obj([True, angM, center[0], center[1]])
      out.draw(frame)
      
  	  
  debugFrame("out", frame)
  return out

def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
	cv2.imshow(name, frame)
  
