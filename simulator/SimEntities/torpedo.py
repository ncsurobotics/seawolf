import cv2
#radius of wheel in meters
RAD = .495

#DB if true, shows graph of where Entity is relative to robot
DB = False


#name of the entity
NAME = "Torpedo"

import math
import numpy as np

from dbEntity import dbEntity

from View.Cameras.mesh import Mesh

class Torpedo(object):
  
  """
  location = 1 by 3 array containing the centerpoint of the entity
  colors = the color of the wheel ( (b, g, r), (b, g, r), (b, g, r) )
  """
  def __init__(self, at = [0, 0, 0], color = (255, 255, 255)):
    self.location = np.float32(at)
    self.name = NAME
    self.radius = RAD
    self.color = color
    #degree of direction its facing
    self.spin = 0
    #rate of spinning, no units yet, just counter
    self.rate = 7
    self.mesh = Mesh('wheel.mesh', at, folder='./SimEntities/Meshes/wheel/')
    self.hidden = False

    if DB:
      self.db = dbEntity(self.location, name = self.name)
  
  def draw(self, roboPos, COBM, camera):
    if DB:
      self.db.draw(roboPos, COBM, camera)
    pt = np.dot(COBM, (self.location - roboPos))
    camera.drawSlice(pt, self.radius, self.spin, 75 + self.spin, (20, 20, 20) )
    camera.drawSlice(pt, self.radius, 75 + self.spin, 150 + self.spin, (0, 0, 255) )
    camera.drawSlice(pt, self.radius, 150 + self.spin, 180 + self.spin, (0, 255, 0) )
    camera.drawSlice(pt, self.radius, 180 + self.spin, 255 + self.spin, (20, 20, 20) )
    camera.drawSlice(pt, self.radius, 255 + self.spin, 330 + self.spin, (0, 0, 255) )
    camera.drawSlice(pt, self.radius, 330 + self.spin, 360 + self.spin, (0, 255, 0) )
    #print "Pic is ", self.pic != None
    #camera.drawImg(pt, self.radius, img=self.pic)

    self.spin += self.rate
    self.spin = self.spin % 360
    return
  
  def update(self):
    self.mesh.turn(.04)
 
  def loc(self):
    return self.location  
  
  def getName(self):
    return self.name
