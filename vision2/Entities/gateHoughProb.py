import cv2
import numpy as np
import math
from Utilities import GatePole as Pole
from Utilities import norm
from Utilities import dist
from VisObj import visObjects


visObj = "gate"
obj = visObjects[visObj]
keys = (obj([False, 0, 0])).keys

def ProcessFrame(frame):
  print("called")
  out = obj([False, 0, 0])
  frameOut = frame.copy()
  frame = norm(frame)
  mean, std = cv2.meanStdDev(frame)
  print "r mean: %d" % (mean[2])
  r = dist(frame, (mean[0], mean[1], 255))
  mean, std = cv2.meanStdDev(r)
  print "m: %d, std %d" % (mean, std)
  #r = frame[:, :, 2]
  r = cv2.GaussianBlur(r, (9, 9), 0)
  debugFrame("red", r)
  std = std if std > 6 else 6
  edges = cv2.Canny(r, std * 1.8, std * 1.8)
  debugFrame("edges", edges)

  lines = cv2.HoughLinesP(edges, 4, math.pi/180, 40, minLineLength = 70, maxLineGap = 10)
  poles = []
  if isinstance(lines, np.ndarray) and (len(lines[0]) > 20):
    return out
  if isinstance(lines, np.ndarray):
    print "numLines: %d" % len(lines[0])
    for line in lines[0]:
      p1 = (line[0], line[1])
      p2 = (line[2], line[3])
      dx = p1[0] - p2[0]
      dy = abs(p1[1] - p2[1])
      theta = math.atan2(dy, dx)
      cv2.line(frameOut, p1, p2, (255, 0, 0), 5)
      if abs(theta - math.pi/2) <  10 *math.pi/180:
        cv2.line(frameOut, p1, p2, (255, 0, 255), 5)
        poles.append(Pole(p1, p2))

  #filtering out the matching poles
  poles = sorted(poles, key = sortPoles)
  if len(poles) > 0:
    gatePoles = [poles[0]]
    for pole in poles:
      if abs(pole.getX() - gatePoles[-1].getX()) < 80:
        #this is the same pole, by inputting it to current pole, the current pole becomes an average of the locations
        gatePoles[-1].add(pole)
        
      else:
        #this is a different pole
        gatePoles.append(pole)
     
    for pole in gatePoles:
      cv2.line(frameOut, pole.p1, pole.p2, (0, 0, 255), 10)
    if len(gatePoles) == 2:
      out = obj([True, gatePoles[0].getX(), gatePoles[1].getX()])
     
    
    print "len Poles: %d, len gatePoles: %d" % (len(poles), len(gatePoles))
  
  
  frameOut = out.draw(frameOut)
  debugFrame("houghProb", frameOut)
  print "-------------------------------"
  
  return out 
  
def sortPoles(pole):
  return pole.getX()

def debugFrame(name, frame):
  cv2.imshow(name, frame) 
