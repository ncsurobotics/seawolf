
diceSideLen = .2286

#DB if true, shows graph of where Entity is relative to robot
DB = False


#name of the entity
NAME = "Dice"

import math
import numpy as np

from dbEntity import dbEntity

class Dice(object):
  
  """
  location = 1 by 3 array containing the centerpoint of the entity
  orientation = the orientation of the path in degrees, relative to forward/y axis
  """
  def __init__(self, at = [0, 0, 0], orientation = 0):
    self.location = np.float32(at)
    self.orientation = -1 * orientation * math.pi/180
    self.name = NAME
    
    line = np.float32([math.sin(self.orientation), 0,  math.cos(self.orientation)])

    widthLine = np.float32([math.cos(self.orientation), 0, -1*math.sin(self.orientation)])
    
    
    p1 = self.location - diceSideLen/2 * line - widthLine/2 * diceSideLen
    p2 = self.location - diceSideLen/2 * line + widthLine/2 * diceSideLen
    p3 = self.location + diceSideLen/2 * line + widthLine/2 * diceSideLen
    p4 = self.location + diceSideLen/2 * line - widthLine/2 * diceSideLen
    
    self.points = [p1, p2, p3, p4]


    self.color = (255, 255, 255)
    if DB:
      self.db = dbEntity(self.location, name = self.name)
  
  def draw(self, roboPos, COBM, camera):
    if DB:
      self.db.draw(roboPos, COBM, camera)
    pts = []
    
    for pt in self.points:
      pts.append(np.dot(COBM, pt - roboPos))
    
    camera.drawPoly(pts, self.color)
    
    
    return
 
 
  def loc(self):
    return self.location  
  
  def getName(self):
    return self.name
