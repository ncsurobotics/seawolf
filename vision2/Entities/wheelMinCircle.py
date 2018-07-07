import cv2
import numpy as np
import math
from Utilities import norm
from Utilities import dist
from Utilities import bcluster
from VisObj import visObjects
import time
import random

visObj = "buoys"
obj = visObjects[visObj]
keys = obj().out.keys()
seeCircles = True


"""
Process Overview:
Finds circles in image
Finds lines (may need to only select lines near circles).
Find intersections of lines and get average intersection: this is near the circle center
Choose the circle with center closest to this average point
"""

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
  edges = cv2.Canny(r, std * 2.5,  1.2* std)
  debugFrame("edges", edges)
  height, width = frame.shape[:2]
  outImg = np.zeros((height,width,3), np.uint8)
  #frameOut = outImg
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

  """ Find and make list of circles in the image """
  
  drawAvg = False
  circleList = []

  minDeg = 80.0
  s = .8
  d = 3.7 
  maxrad = 150
  minrad = 30
  step = 50
  for radius in range(minrad + step, maxrad + 1, step):
    circles =  cv2.HoughCircles(image = r, method = cv2.cv.CV_HOUGH_GRADIENT, dp = 4.2, minDist =  2 * radius, param2 = int((2 * radius * math.pi)/8.94), minRadius = radius - step, maxRadius = radius)
    msg = "minRadius: %d, maxRadius %d" % (radius - step, radius)
    if type(circles) != type(None):
      print msg + " found: %d" % (len(circles))
      for circ in circles[0,:]:
        circleList.append(circ)
        if seeCircles:
          cv2.circle(frameOut, (circ[0], circ[1]), circ[2], (0,0,0), 2, 8, 0 )
    else:
      print msg + " no circ found"
  if len(circleList) > 2:
    pts = []
    for circle in circleList:
      #out.append(circle)
      if seeCircles:
        cv2.circle(frameOut, (int(circle[0]), int(circle[1])), int(circle[2]), (255,0,0), 2, 8, 0 )
        cv2.circle(frameOut, (int(circle[0]), int(circle[1])), 7, (0,0,0), 2, 8, 0 )
      pts.append([circle[0], circle[1]])
    contour = np.array(pts, dtype=np.int32)
    (x,y), r = cv2.minEnclosingCircle(contour)
    out.append([int(x), int(y), int(r)])
    #cv2.circle(frameOut, (int(x), int(y)), int(r), (0,0,0), 2, 8, 0 )
    
  
  frameOut = out.draw(frameOut)
  out.draw(frameOut)

  debugFrame("houghProb", frameOut)
  print "-------------------------------"
  
  return out
  
def sortPoles(pole):
  return pole[0][0]

def debugFrame(name, frame):
  cv2.imshow(name, frame) 
