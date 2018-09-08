"""
implementation of the gate vision obj
"""
import numpy as np
import cv2
from visobj import VisObj
import math

keys = ["found", "orientation", "centerPointX", "centerPointY"]

class pathVisObj(VisObj):

  
  # array of [found, orientation, cx, cy]
  def __init__(self, data):
    if str(data[0]) == str(False):
      data[0] = False
    self.found = bool(data[0])
    self.orientation = float(data[1])
    self.cx = int(data[2])
    self.cy = int(data[3])
    self.keys = keys
    self.out = {}
    self.out["found"] = self.found
    self.out["centerPointX"] = self.cx
    self.out["centerPointY"] = self.cy
    self.out["orientation"] = self.orientation
    
    
  def draw(self, frame):
    if not self.found:
      return frame
    frameOut = np.copy(frame)
    maxx, maxy, _ = frame.shape
    x = self.cx
    y = self.cy
    xv = -1 * math.sin(math.pi * self.orientation/180.0)
    yv = -1 * math.cos(math.pi * self.orientation/180.0)
    p1 = [x, y]
    p2 = [x, y]
    maxy, maxx, _ = frame.shape
    while p2[0] < maxx and p2[0] > 0 and p2[1] < maxy and p2[1] > 0:
        p2[1] += yv
        p2[0] += xv
    
    cv2.line(frameOut, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (0, 255, 0))
    return frameOut
