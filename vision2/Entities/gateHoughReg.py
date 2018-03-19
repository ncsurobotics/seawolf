import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from VisObj import visObjects


visObj = "gate"
obj = visObjects[visObj]
keys = (obj([False, 0, 0])).keys

def ProcessFrame(frame):
  out = obj([False, 0, 0])
  frameOut = frame.copy()
  frame = norm(frame)
  mean, std = cv2.meanStdDev(frame)
  print mean
  r =  cv2.cvtColor(frameOut, cv2.COLOR_BGR2GRAY)
  mean, std = cv2.meanStdDev(r)
  print "m: %d, std %d" % (mean, std)
  #r = frame[:, :, 2]
  debugFrame("COI", r)
  r = cv2.GaussianBlur(r, (7, 7), 0)
  edges = cv2.Canny(r, std * 2.0 , 1.3 * std)
  debugFrame("edges", edges)
  

  lines = cv2.HoughLines(edges, 3, math.pi/180, 110)
  poles = []
  if lines is list:
    print "numLines: %d" % len(lines[0])
    for line in lines[0]:
      r = line[0]
      theta = line[1]
      if ( abs(theta - round((theta/math.pi)) * math.pi) < 3.0 * math.pi / 180.0):
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * r
        y0 = b * r
        pt1 = (int(x0 - 100*b), int(y0 + 100 * a))
        pt2 = (int(x0 + 100 * b), int(y0 - 100 * a))
        poles.append(((x0, y0), pt1, pt2))
        cv2.line(frameOut, pt1, pt2, (255, 0, 255), 5)
  
  #filtering out the matching poles
  poles = sorted(poles, key = sortPoles)
  if len(poles) > 0:
    gatePoles = [poles[0]]
    for pole in poles:
      if abs(pole[0][0]  - gatePoles[-1][0][0]) > 80:
        gatePoles.append(pole)
    for pole in gatePoles:
      cv2.line(frameOut, pole[1], pole[2], (0, 0, 255), 10)
    if len(gatePoles) == 2:
      out = obj([True, gatePoles[0][0][0], gatePoles[1][0][0]])
     
    
    print "len Poles: %d, len gatePoles: %d" % (len(poles), len(gatePoles))
  
  
  frameOut = out.draw(frameOut)
  debugFrame("houghReg", frameOut)
  print "-------------------------------"
  
  return out  
  
def sortPoles(pole):
  return pole[0][0]

def debugFrame(name, frame):
  cv2.imshow(name, frame) 
