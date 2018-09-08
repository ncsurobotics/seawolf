"""
implementation of the bent path vision object
"""
import numpy as np
import cv2
from visobj import VisObj
import math

keys = ["found", "centerPointX", "centerPointY", "point1X", "point1Y", "point2X", "point2Y" ]

class pathBentVisObj(VisObj):

  
  # array of [found, orientation, cx, cy]
  def __init__(self, data):
    if str(data[0]) == str(False):
      data[0] = False
    self.found = bool(data[0])
    self.cx = int(data[1])
    self.cy = int(data[2])
    self.p1x = int(data[3])
    self.p1y = int(data[4])
    self.p2x = int(data[5])
    self.p2y = int(data[6])
    
    self.keys = keys
    self.out = {}
    self.out["found"] = self.found
    self.out["centerPointX"] = self.cx
    self.out["centerPointY"] = self.cy
    self.out["point1X"] = self.p1x
    self.out["point1Y"] = self.p1y
    self.out["point2X"] = self.p2x
    self.out["point2Y"] = self.p2y
    
  def draw(self, frame):
    if not self.found:
      return frame
    frameOut = np.copy(frame)
    """
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
    """
    cv2.line(frameOut, (int(self.cx), int(self.cy)), (int(self.p1x), int(self.p1y)), (0, 255, 0), thickness=3)
    cv2.line(frameOut, (int(self.cx), int(self.cy)), (int(self.p2x), int(self.p2y)), (0, 255, 0), thickness=3)
    cv2.circle(frameOut, (int(self.p1x), int(self.p1y)), 5, (0, 0, 0), -1)
    cv2.circle(frameOut, (int(self.p2x), int(self.p2y)), 5, (0, 0, 0), -1)
    cv2.circle(frameOut, (int(self.cx), int(self.cy)), 5, (0, 0, 0), -1)
    cv2.circle(frameOut, (int(self.p1x), int(self.p1y)), 3, (0, 0, 255), -1)
    cv2.circle(frameOut, (int(self.p2x), int(self.p2y)), 3, (255, 0, 0), -1)
    cv2.circle(frameOut, (int(self.cx), int(self.cy)), 3, (0, 255, 0), -1)
    
    return frameOut

    def center(self):
        return [self.cx, self.cy]

    def endPoints(self):
        return [[self.p1x, self.p1y], [self.p2x, self.p2y]]