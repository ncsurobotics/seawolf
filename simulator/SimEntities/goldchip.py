#symbolizes Get Gold Chip object from Competition Documentation
#Height of the pole section (estimated because rulebook does not say measurement explicitly)
poleHeight = 2.5
#Diameter of the pole section
poleDiameter = .052
#Radius of the Gold Plate (4 in = .1016 m)
plateRadius = .1

#DB if true, shows graph of where Entity is relative to robot
DB = False


#name of the entity
NAME = "GoldChip"


import math
import numpy as np

from dbEntity import dbEntity

class GoldChip(object):
  
  """
  input dict is expected to contain the following
  at = 1 by 3 array containing the centerpoint of the entity
  orientation = angles in degrees from the y axis
  """
  def __init__(self, at = [0, 0, 0], orientation = 0):
    self.location = np.float32(at)
    self.name = NAME
    self.radius = plateRadius
    #degree of direction its facing
    self.spin = 0
    
    #degrees into radians
    orientation = math.pi/180 * orientation
    height = np.float32([0, 0, 1]) * poleHeight
    
    #making the pole by subtracting the components of the location array by the height array components
    #p1 is placed 3/4 the height of the pole below the center of the entity to make plate appear closer to the top
    p1 = self.location - height*3/4
    p2 = self.location + height/4
    self.poles = [p1, p2]

    #color of the pole
    self.color = (255, 255, 255) 
    #color of the "$" plate
    self.color2 = (0, 255, 255)
  
    if DB:
      self.db = dbEntity(self.location, name = self.name)
    
    return

  def draw(self, roboPos, COBM, camera):
    if DB:
      self.db.draw(roboPos, COBM, camera)

    #making the pole of the Gold Chip mechanism
    pts  = []
    for pt in self.poles:
      pts.append(np.dot(COBM, pt - roboPos))
    camera.drawLine(pts[0], pts[1], color = self.color, thickness = poleDiameter)

    #making the "$" plate of the Gold Chip mechanism
    pt = np.dot(COBM, (self.location - roboPos))
    camera.drawCirc(pt, self.radius, self.color2)

    return
 
 
  def loc(self):
    return self.location 
    
    
  def getName(self):
    return self.name 




