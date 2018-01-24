import cv2
import numpy as np
from Utilities import dist
from Utilities import norm
from VisObj import visObjects


visObj = "gate"
obj = visObjects[visObj]
keys = (obj([False, 0, 0])).keys

def ProcessFrame(frame):
  out = obj([False, 0, 0])
  frameOut = np.copy(frame)
  frame = norm(frame)
  m = cv2.mean(frame)
  red = dist(frame, [m[0],  m[1], 255])
  debugFrame("red", red)
  (row, col, pages) = frame.shape
  maxArea = 30000
  minArea = 1000
  ret, thresh = cv2.threshold(red, np.mean(red) - np.std(red) * 1.75, 255, cv2.THRESH_BINARY_INV)
  kernel = np.ones((5,5),np.uint8)
  debugFrame("threshOg", thresh)
  thresh = cv2.erode(thresh,kernel, iterations = 1)
  thresh = cv2.dilate(thresh, kernel, iterations = 2)
  debugFrame("thresh", thresh)
  contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  possiblePoles = []
  for cont in contours:
    #cv2.drawContours(frame, [cont], -1, (0, 0, 255), 3)
    (center, (w, h), ang) = cv2.minAreaRect(cont)
    area = w * h
    if w > 0:
      aspectRatio = h / w
      if aspectRatio < 1 and aspectRatio != 0:
    	  aspectRatio = 1/aspectRatio
    	  ang+=90
    else:
      aspectRation = 20
    angp = abs(ang)
    angp = abs(angp - round((angp/180.0)) * 180)
    stringOut = "%d %d %d" % (angp, area, aspectRatio)
    cv2.putText(frameOut, stringOut, (int(center[0]), int(center[1])), cv2.FONT_HERSHEY_SIMPLEX, .5, 255)
    if (angp < 10 or angp > 170) and area > minArea and area < maxArea and abs(aspectRatio - 7) <= 3:
      possiblePoles.append((cont, center))
      
    
  possiblePoles = sorted(possiblePoles, key = sortPoles)
  for pole in possiblePoles:
  	  cv2.drawContours(frameOut, [pole[0]], -1, (0, 0, 255), 3)
  	  (center, (w, h), ang) = cv2.minAreaRect(pole[0])
  	  aspectRatio = h / w
  	  if aspectRatio < 1:
  	    ang+=90
  	  angp = abs(ang)
  	  angp = abs(angp - round((angp/180)) * 180)
  	  area = h * w
  	  stringOut = "%d %d %d" % (angp, area, aspectRatio)
  	  cv2.putText(frameOut, stringOut, (int(center[0]), int(center[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
      
  if len(possiblePoles) > 1:
  	prevPole = possiblePoles[0]
  	poles = [prevPole]
  	for pole in possiblePoles:
  	  cv2.drawContours(frame, [pole[0]], -1, (0, 0, 255), 3)
  	  diff = abs( pole[1][0] - prevPole[1][0])
  	  if (diff > 20):
  	    poles.append(pole)
  	  prevPole = pole 
  	if (len(poles) == 2):
  	  left = poles[0]
  	  right = poles[1]
  	  out = obj([True, int(right[1][0]), int(left[1][0])])
  	  frameOut = out.draw(frameOut)
  	  cv2.drawContours(frameOut, [left[0], right[0]], -1, (0,0, 0), 3) 
  	  
  debugFrame("out", frameOut)
  return out.dict()

def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
  a = 1
  cv2.imshow(name, frame)
  
