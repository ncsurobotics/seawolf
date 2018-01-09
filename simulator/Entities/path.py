
#length of path in meters
pathLength = 1.0
#widht of paht in meters
pathWidth = .5

#DB if true, shows graph of where Entity is relative to robot
DB = False


#name of the entity
NAME = "Path"

import math
import numpy as np

from dbEntity import dbEntity

class Path(object):
  
  """
  location = 1 by 3 array containing the centerpoint of the entity
  orientation = the orientation of the path in degrees, relative to forward/y axis
  """
  def __init__(self, location = [0, 0, 0], orientation = 0):
    self.location = np.float32(location)
    self.orientation = orientation * math.pi/180
    self.name = NAME
    line = np.float32([math.sin(self.orientation), math.cos(self.orientation), 0])
    widthLine = np.float32([math.cos(self.orientation), -1*math.sin(self.orientation), 0])
    
   
    p1 = self.location - pathLength/2 * line - widthLine/2 * pathWidth
    p2 = self.location - pathLength/2 * line + widthLine/2 * pathWidth
    p3 = self.location + pathLength/2 * line + widthLine/2 * pathWidth
    p4 = self.location + pathLength/2 * line - widthLine/2 * pathWidth
    
    
    self.points = [p1, p2, p3, p4]
    
    self.color = (0, 0, 255)
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
