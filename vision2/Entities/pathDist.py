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
  frameOut = np.copy(frame)
  frame = norm(frame)
  m = cv2.mean(frame)
  red = dist(frame, [m[0],  m[1], 255])
  debugFrame("red", red)
  (row, col, pages) = frame.shape
  maxArea = (row * col)/3
  minArea = 200
  red = cv2.medianBlur(red, ksize = 3)
  ret, thresh = cv2.threshold(red, np.mean(red) - max(np.std(red), 10) * 2.65, 255, cv2.THRESH_BINARY_INV)
  debugFrame("threshOg", thresh)
  kernel = np.ones((7,7),np.uint8)
  thresh = cv2.erode(thresh,kernel, iterations = 2)
  debugFrame("thresh", thresh)
  contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  for cont in contours:
    if len(cont) < 3:
      continue
    (center, (w, h), ang) = cv2.minAreaRect(cont)
    area = w * h
    aspectRatio = 0
    if w != 0:
      aspectRatio = h / w
      if aspectRatio < 1 and aspectRatio != 0:
    	  aspectRatio = 1/aspectRatio
    	  ang+=90
    else:
      aspectRatio = 1
    
    #caluclating solidity
    contArea = cv2.contourArea(cont)
    if contArea < .1:
      conArea = 1.0
    
    if area == 0:
      area = 1
    
    solidity = contArea / (1.0 * area)
    loc = (int(center[0]), int(center[1]))
    stringOut = "%f" % (solidity)
    #cv2.putText(frameOut, stringOut, loc, cv2.FONT_HERSHEY_SIMPLEX, .5, 255)
    
    if area > 1500 and aspectRatio > 3 and aspectRatio < 13 and solidity > .8:
      angp = -1 * ang
      #angp = angp - round((angp/180.0)) * 180
      stringOut += ", ang: %d" % (angp)
      cv2.drawContours(frameOut, [cont], -1, (0,0, 0), 3)
      out = obj([True, angp, center[0], center[1]])
      frameOut = out.draw(frameOut)
    cv2.putText(frameOut, stringOut, loc, cv2.FONT_HERSHEY_SIMPLEX, .5, 255)
    print stringOut
  	  
  debugFrame("out", frameOut)
  return out

def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
	cv2.imshow(name, frame)
  
