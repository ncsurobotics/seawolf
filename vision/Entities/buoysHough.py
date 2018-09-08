import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from VisObj import visObjects


visObj = "buoys"
obj = visObjects[visObj]
keys = obj().out.keys()

def ProcessFrame(frame):
  out = obj()
  frameOut = frame.copy()
  frame = norm(frame)
  mean, std = cv2.meanStdDev(frame)
  r = dist(frame, (mean[0], mean[1], mean[2]))
  mean, std = cv2.meanStdDev(r)
  print "m: %d, std %d" % (mean, std)
  #r = frame[:, :, 2]
  r = cv2.GaussianBlur(r, (9, 9), 0)
  debugFrame("ChannelOfInterest", r)
  edges = cv2.Canny(r, std * 3.5,  1.2* std)
  debugFrame("edges", edges)
  

  lines = cv2.HoughLinesP(edges, 4, math.pi/180, 200, minLineLength = 100, maxLineGap = 50)
  if isinstance(lines, list):
    print "numLines: %d" % len(lines[0])
    for line in lines[0]:
      p1 = (line[0], line[1])
      p2 = (line[2], line[3])
      dx = p1[0] - p2[0]
      dy = abs(p1[1] - p2[1])
      theta = math.atan2(dy, dx)
      if abs(theta - math.pi/2) <  10 *math.pi/180:
        cv2.line(frameOut, p1, p2, (255, 0, 255), 5)
  
  """
  Below is the param info for HoughCircles
    image is the imaged being looked at by the function
    method cv2.CV_HOUGH_GRADIENT is the only method available
    dp the size of accumulator inverse relative to input image, dp = 2 means accumulator is half dim of input image
    minDist minimum distance between detected circles, too small and mult neighbor circ founds, big and neighbor circ counted as same
    param1 bigger value input into canny, unsure why it is useful therefore not using
    param2 vote threshold
    minRadius  min Radius of circle to look for
    maxRadius  max Radius of circle to look for
  """
  maxrad = 300
  minrad = 10
  step = 50
  for radius in range(minrad + step, maxrad + 1, step):
    circles =  cv2.HoughCircles(image = r, method = cv2.cv.CV_HOUGH_GRADIENT, dp = .5, minDist =  radius * 2, param2 = int((2 * radius * math.pi)/15), minRadius = radius - step, maxRadius = radius)
    msg = "minRadius: %d, maxRadius %d" % (radius - step, radius)
    if type(circles) != type(None):
      print msg + " found: %d" % (len(circles))
      for circ in circles[0,:]:
        out.append(circ)
        out.draw(frameOut)
        
    else:
      print msg + " no circ found"
      
  
  
  frameOut = out.draw(frameOut)
  debugFrame("houghProb", frameOut)
  print "-------------------------------"
  
  return out
  
def sortPoles(pole):
  return pole[0][0]

def debugFrame(name, frame):
  cv2.imshow(name, frame) 
