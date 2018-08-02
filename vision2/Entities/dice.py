import cv2
import numpy as np
from Utilities import dist
from Utilities import norm
from VisObj import visObjects

minArea = 700
maxArea = 300
visObj = "gate"
obj = visObjects[visObj]
keys = (obj([False, 0, 0])).keys

def ProcessFrame(frame):
  out = obj([False, 0, 0])
  frameOut = frame.copy()
  frame = norm(frame)
  mean, std = cv2.meanStdDev(frame)
  print "r mean: %d" % (mean[2])
  r = dist(frame, (mean[0], mean[1], max(mean[2], 80)))
  mean, std = cv2.meanStdDev(r)
  print "m: %d, std %d" % (mean, std)
  #r = frame[:, :, 2]
  r = cv2.GaussianBlur(r, (9, 9), 0)
  debugFrame("red", r)
  if std > 6:
    edges = cv2.Canny(r, std * 2.0, std * 1.1)
  else:
    edges = cv2.Canny(r, 30 , 20)
  debugFrame("edges", edges)
  contours, _ = cv2.findContours(r, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  possiblePoles = []
  for cont in contours:
    cv2.drawContours(frame, [cont], -1, (0, 0, 255), 3)
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
    if (angp < 10 or angp > 170) and area > minArea and area < maxArea and abs(aspectRatio) <= 2:
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
  return out

def sortPoles(pole):
  
  return pole[1][0]

def debugFrame(name, frame):
  a = 1
  cv2.imshow(name, frame)
  
