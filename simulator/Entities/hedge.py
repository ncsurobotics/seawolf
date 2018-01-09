
#length of gate in meters
gateLength = 1.0
#widht of gate in meters
gateWidth = 2.0
#poleDiameter
poleDiameter = .1

#DB if true, shows graph of where Entity is relative to robot
DB = False


#name of the entity
NAME = "Hedge"

import math
import numpy as np

from dbEntity import dbEntity

class Hedge(object):
  
  """
  location = 1 by 3 array containing the centerpoint of the entity
  orientation = angles in degree rotated from y axis
  """
  def __init__(self, location = [0, 0, 0], orientation = 0):
    self.location = np.float32(location)
    self.name = NAME
    orientation = math.pi/180 * orientation
    length = np.float32([0, 0, 1]) * gateLength
    width  = np.float32([math.cos(orientation), math.sin(orientation), 0]) * gateWidth
    
    self.poles = []
    
    #making the first pole
    p1 = self.location - length/2  - width/2
    p2 = self.location + length/2  - width/2
    self.poles.append([p1, p2])
    
    #making the seccond pole
    p3 = self.location - length/2  + width/2
    p4 = self.location + length/2  + width/2
    self.poles.append([p3, p4])
    
    #making the bottom pole
    self.poles.append([p1, p3])
    
    self.color = (0, 255, 100)
    
    if DB:
      self.db = dbEntity(self.location, name = self.name)
    
    return
  
  def draw(self, roboPos, COBM, camera):
    if DB:
      self.db.draw(roboPos, COBM, camera)
    
    for pole in self.poles:
      pts  = []
      for pt in pole:
        pts.append(np.dot(COBM, pt - roboPos))
      camera.drawLine(pts[0], pts[1], color = self.color, thickness = poleDiameter)
    return
 
 
  def loc(self):
    return self.location  
    
  def getName(self):
    return self.name
