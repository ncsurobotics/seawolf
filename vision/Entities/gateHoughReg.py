import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from VisObj import visObjects
from Utilities import debugFrame
from math import pi


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
  edges = cv2.Canny(r, std * 1.0 , 1.3 * std)
  debugFrame("edges", edges)
  
  lineDict = {}

  minLineLength = 100
  maxLineGap = 10

  DEG_NUM = 36

  lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
  poles = []
  if lines.__class__.__name__ != 'NoneType':
    for x0,y0,x1,y1 in lines[0]:
      cv2.line(frameOut,(x0,y0),(x1,y1),(255,0,255),5)
      theta = math.atan2(y1-y0, x1-x0)
      r = math.sqrt((y1 - y0) ** 2 + (x1 - x0) ** 2)
      
      deg = theta * 180 / pi
      # slice in pizza pie with DEG_NUM slices
      deg_slice = int(DEG_NUM * (deg / 360))

      if deg_slice in lineDict:
        lineDict[deg_slice].append((x0,y0,r,theta))
      else:
        lineDict[deg_slice] = [(x0,y0,r,theta)]

  else:
    print "Lines is", lines.__class__.__name__

  print "LINE DICT LEN IS", len(lineDict)
  for deg_slice in lineDict:
    lines = lineDict[deg_slice]
    for line in lines:
      x0,y0,r,theta = line
      col = 255 - abs(deg_slice / DEG_NUM) * 255
      pt1 = int(x0), int(y0)
      pt2 = int(x0 + r * math.cos(theta)), int(y0 + r * math.sin(theta))
      cv2.line(frameOut, pt1, pt2, (col, 0, col), 5)
  
  #filtering out the matching poles
  poles = sorted(poles, key = sortPoles)
  if len(poles) > 0:
    gatePoles = [poles[0]]
    for pole in poles:
      if abs(pole[0][0]  - gatePoles[-1][0][0]) > 80:
        gatePoles.append(pole)
    #for pole in gatePoles:
      #cv2.line(frameOut, pole[1], pole[2], (0, 0, 255), 10)
    if len(gatePoles) == 2:
      out = obj([True, gatePoles[0][0][0], gatePoles[1][0][0]])
     
    
    print "len Poles: %d, len gatePoles: %d" % (len(poles), len(gatePoles))
  
  
  frameOut = out.draw(frameOut)
  debugFrame("houghReg", frameOut)
  print "-------------------------------"
  
  return out  
  
def sortPoles(pole):
  return pole[0][0]
  