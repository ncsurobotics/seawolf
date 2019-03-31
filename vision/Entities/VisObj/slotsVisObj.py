"""
implementation of the gate vision obj
"""
import numpy as np
import cv2
from visobj import VisObj
import math
import time

class HoleRecord:
  def __init__(self, time, hole):
    self.time = time
    self.hole = hole

"""
sparse grid of hole records
can be thought of as grid where each unit has a list of holes in it
"""
class History:
  def __init__(self):
    # length coords need to be close by
    self.coord_length = 20
    # rows = { x1 : { y1 : HoleRecord}, x4 : { y2 : HoleRecord}, ... }
    self.rows = {}
  
  # add a record to the grid
  def addRecord(self, holeRecord):
    x,y,w,h = holeRecord.hole
    x_group = int(x/self.coord_length)
    y_group = int(y/self.coord_length)
    if x_group not in self.rows:
      self.rows[x_group] = {}
      print "appeneded to x"
    if y_group not in self.rows[x_group]:
      self.rows[x_group][y_group] = []
      print "appened to y"
    self.rows[x_group][y_group].append(holeRecord)

  # remove records older than age ago (age is in seconds)
  def clearRecords(self, age):
    now = time.time()
    last_old = -1
    for x_group in self.rows:
      for y_group in self.rows[x_group]:
        for i in range(1, len(self.rows[x_group][y_group])):
          record = self.rows[x_group][y_group][i]
          # if current record is less than
          if now - record.time >= age:
            last_old = i
        if last_old != -1:
          self.rows[x_group][y_group] = self.rows[x_group][y_group][last_old + 1: len(self.rows[x_group][y_group])]

    
    

keys = ["found", "locations"]
# coords 
history = History()


class slotsVisObj(VisObj):

  keys = ["found", "locations"]
  history = {}

  def __init__(self, data):
    self.found = data[0]
    self.locations = data[1]
    self.out = {"found" : False, "locations" : []}
    # time it takes points drawn points to fade from memory
    self.fadeTime = .15
  
  def updateHistory(self, holes):
    for hole in holes:
      record = HoleRecord(time.time(), hole)
      history.addRecord(record)
    history.clearRecords(self.fadeTime)
  
  def historyPoints(self, thresh):
    pts = []
    for x in history.rows:
      for y in history.rows[x]:
        repeats = len(history.rows[x][y])
        if repeats >= thresh:
          pts.append((x, y))
    return pts
    
  def draw(self, frame):
    
    if not self.found:
      return frame
    
    for x, y, w, h in self.locations:
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),-1)
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
      cv2.rectangle(frame,(x + w/2 - 2,y + h/2 -2),(x + w/2 + 2, y + h/2 + 2),(0,0,255),-1)
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