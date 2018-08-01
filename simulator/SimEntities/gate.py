
#length of gate in meters
gateLength = 1.2
#widht of gate in meters
gateWidth = 3.0
#poleDiameter
poleDiameter = .052

#red patch
patchL = 1.220
patchW = .2
shiftP = 1


#DB if true, shows graph of where Entity is relative to robot
DB = False


#name of the entity
NAME = "Gate"


import math
import numpy as np

from dbEntity import dbEntity

class Gate(object):
  
  """
  input dict is expected to contain the following
  at = 1 by 3 array containing the centerpoint of the entity
  orientation = angles in degrees from the y axis
  """
  def __init__(self, at = [0, 0, 0], orientation = 0):
    self.location = np.float32(at)
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
    p1 = self.location - length/2  + width/2
    p2 = self.location + length/2  + width/2
    self.poles.append([p1, p2])
    
    #making the red bar
    downLine = np.float32([0, 0, 1])
    widthLine = np.float32([math.cos(orientation), math.sin(orientation), 0])
    
   
    p1 = self.location - patchL/2 * downLine - widthLine/2 * patchW + [shiftP, 0, 0]
    p2 = self.location - patchL/2 * downLine + widthLine/2 * patchW + [shiftP, 0, 0]
    p3 = self.location + patchL/2 * downLine + widthLine/2 * patchW + [shiftP, 0, 0]
    p4 = self.location + patchL/2 * downLine - widthLine/2 * patchW + [shiftP, 0, 0]
    
    self.patch = [p1, p2, p3, p4]
    
    self.color = (0, 0, 255)
    
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
    
    #drawing the patch
    pts = []
    for pt in self.patch:
      pts.append(np.dot(COBM, pt - roboPos))
    
    camera.drawPoly(pts, self.color)
    
    return
 
 
  def loc(self):
    return self.location 
    
    
  def getName(self):
    return self.name 
