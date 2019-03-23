"""
implementation of the gate vision obj
"""
import numpy as np
import cv2
from visobj import VisObj
import math

keys = ["found", "locations"]

class slotsVisObj(VisObj):

  keys = ["found", "locations"]

  def __init__(self, data):
    self.found = data[0]
    self.locations = data[1]
    self.out = {"found" : False, "locations" : []}
    
  def draw(self, frame):
    
    if not self.found:
      return frame
    for x, y, w, h in self.locations:
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),-1)
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
      cv2.rectangle(frame,(x + w/2 - 2,y + h/2 -2),(x + w/2 + 2, y + h/2 + 2),(0,0,255),-1)
      
      print "VISOBJ", self.found
    return frame
  
  """
  returns closest location to the center of the screen
  """
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