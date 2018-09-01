"""
implementation of the gate vision obj
"""
import numpy as np
import cv2
from visobj import VisObj

keys = ["found", "leftPole", "rightPole", "center"]
class gateVisObj(VisObj):

  
  # array of [found, leftPole, rightPole]
  def __init__(self, data):
    if str(data[0]) == str(False):
      data[0] = False
    self.found = data[0]
    self.lp = int(data[1])
    self.rp = int(data[2])
    self.cp = self.lp + (self.rp - self.lp)/2
    self.out = {}
    self.keys = keys
    self.out["found"] = self.found
    self.out["leftPole"] = self.lp
    self.out["rightPole"] = self.rp
    self.out["center"] = self.cp
    
    
  def draw(self, frame):
    if not self.found:
      return frame
    r,c,_ = frame.shape
    frameOut = np.copy(frame)
    if (self.found):
      cv2.circle(frameOut, (self.cp, int(r/2)), 10, (0, 0, 255), 3)
      cv2.putText(frameOut, str(self.cp - c/2),(self.cp + 6, int(r/2)), cv2.FONT_HERSHEY_SIMPLEX, .5, 255)  
    return frameOut
  
  """
  returns the center point of the gate in the frame, pixels to the right 
  """
  def loc(self):
    return self.cp
