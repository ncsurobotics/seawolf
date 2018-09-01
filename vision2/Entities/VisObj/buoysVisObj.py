"""
implementation of the gate vision obj
"""
import numpy as np
import cv2
from visobj import VisObj
import math

keys = ["found", "locX", "locY"]

class buoysVisObj(VisObj):

  

  def __init__(self):
    self.locations = []
    self.found = False
    self.out = {"found" : False, "locX" : 0, "locY" : 0}
  
  
  def append(self, circle):
    """
    input: circle is tuple of (x, y, r)
    """
    self.locations.append(circle)
    self.out["found"] = True
    self.out["locX"] = circle[0]
    self.out["locY"] = circle[1]
    self.found = True
    self.cp = (int(circle[0]), int(circle[1]))
    self.r = int( circle[2] )
    
  def draw(self, frame):
    if not self.found:
      return frame
    r,_,_ = frame.shape
    frameOut = np.copy(frame)
    for loc in self.locations:
      cv2.circle(frameOut, (loc[0], loc[1]), loc[2], (255, 51, 255), 3)
      cv2.circle(frameOut, (loc[0], loc[1]), 2, (0, 0, 0), 2)
    return frameOut
  
  """
  returns the center point of the gate in the frame, pixels to the right 
  """
  def loc(self):
    return self.cp
  def closestLoc(self, frame):
    h,w,_  = frame.shape
    minDist = math.sqrt( (h/2 - self.locations[0][1]) ** 2 + (self.locations[0][0] - w/2) ** 2)
    closestLoc = self.locations[0]
    for loc in self.locations:
      distFromCenter = math.sqrt( (h/2 - loc[1]) ** 2 + (loc[0] - w/2) ** 2)
      if distFromCenter < minDist:
        minDist = distFromCenter
        closestLoc = loc
    return closestLoc