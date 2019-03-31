import cv2
import numpy as np
import math
from Utilities import GatePole as Pole
from Utilities import norm
from Utilities import dist
from VisObj import visObjects


visObj = "buoys"
obj = visObjects[visObj]
keys = obj().out.keys()

def ProcessFrame(frame):
  print("called")
  out = obj() 
  HEIGHT,WIDTH,_  = frame.shape
  #frame = norm(frame)
  #frame = cv2.GaussianBlur(frame,(25,25),0)
  frameOut = frame.copy()
  th1 = 200
  th2 = th1 * 0.4
  edges = cv2.Canny(frame, th1, th2)
  debugFrame("edges", edges)
  
  # Apply probabilistic hough line transform
  lines = cv2.HoughLinesP(edges, 2, np.pi/180.0, 50, minLineLength=10, maxLineGap=20)
  try:
    for line in lines:
      x1, y1, x2, y2 = line[0]
      cv2.line(frameOut, (x1, y1), (x2, y2), (0,0,0), 3)
  except:
    pass
  
  #contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  #debugFrame("contours", contours)

  """
  if(len(dice) >= 2):
    for die in dice:
      out.append(die)
  """
  frameOut = out.draw(frameOut)

  debugFrame("houghProb", frameOut)
  print "-------------------------------"
  
  return out
  
def sortPoles(pole):
  return pole[0][0]

def debugFrame(name, frame):
  cv2.imshow(name, frame) 
