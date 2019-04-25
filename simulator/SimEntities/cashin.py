#DB if true, shows graph of where Entity is relative to robot
DB = False


#name of the entity
NAME = "CashIn"


import math
import numpy as np

from dbEntity import dbEntity

from View.Cameras.mesh import Mesh

class CashIn(object):
  
  """
  input dict is expected to contain the following
  at = 1 by 3 array containing the centerpoint of the entity
  orientation = angles in degrees from the y axis
  """
  def __init__(self, at = [0, 0, 0], orientation = 0):
    self.location = np.float32(at)
    self.name = NAME

    gateLength = 1
    gateWidth = 1  
    orientation = math.pi/180 * orientation
    length = np.float32([0, 0, 1]) * gateLength
    width  = np.float32([math.cos(orientation), math.sin(orientation), 0]) * gateWidth
    
    self.poles = []
    '''
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
    '''
    self.color = (0, 0, 255)
    self.mesh = Mesh('cashin.mesh', self.location, scale=[.5,.5,.5], orientation=.2, folder='./SimEntities/Meshes/cashin/')
    
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
 
  def update(self):
    #self.mesh.move([0,0,-.25])
    pass
  
  def loc(self):
    return self.location 
    
    
  def getName(self):
    return self.name 
