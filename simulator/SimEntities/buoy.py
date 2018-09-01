
#radius of bouy in meters
RAD = .1

#DB if true, shows graph of where Entity is relative to robot
DB = False


#name of the entity
NAME = "Bouy"

import math
import numpy as np

from dbEntity import dbEntity

class Buoy(object):
  
  """
  location = 1 by 3 array containing the centerpoint of the entity
  color = the color of the bouy (b, g, r)
  """
  def __init__(self, at = [0, 0, 0], color = (0, 0, 255)):
    self.location = np.float32(at)
    self.name = NAME
    self.radius = RAD
    self.color = color
    if DB:
      self.db = dbEntity(self.location, name = self.name)
  
  def draw(self, roboPos, COBM, camera):
    if DB:
      self.db.draw(roboPos, COBM, camera)
    pt = np.dot(COBM, (self.location - roboPos))
    camera.drawCirc(pt, self.radius, self.color)
    return
 
 
  def loc(self):
    return self.location  
  
  def getName(self):
    return self.name
