
#width of slots in meters
WIDTH = 1

#DB if true, shows graph of where Entity is relative to robot
DB = False


#name of the entity
NAME = "Slots"

import math
import numpy as np

from dbEntity import dbEntity

class Slots(object):
  
  """
  location = 1 by 3 array containing the centerpoint of the entity
  color = the color of the bouy (b, g, r)
  """
  def __init__(self, at = [0, 0, 0], color = (81, 84, 95)):
    self.location = np.float32(at)
    self.name = NAME
    self.width = WIDTH
    self.color = color
    if DB:
      self.db = dbEntity(self.location, name = self.name)
  
  def draw(self, roboPos, COBM, camera):
    if DB:
      self.db.draw(roboPos, COBM, camera)
    pt = np.dot(COBM, (self.location - roboPos))
    camera.drawRect(pt, self.width, self.width, self.color)
    return
 
 
  def loc(self):
    return self.location  
  
  def getName(self):
    return self.name
