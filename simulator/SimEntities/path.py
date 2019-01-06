
#length of path in meters
pathLength = 1.2
#widht of paht in meters
pathWidth = .15

#DB if true, shows graph of where Entity is relative to robot
DB = False


#name of the entity
NAME = "Path"

import math
import numpy as np

from dbEntity import dbEntity

from View.Cameras.mesh import Mesh

class Path(object):
  
  """
  location = 1 by 3 array containing the centerpoint of the entity
  orientation = the orientation of the path in degrees, relative to forward/y axis
  theta = the amount the path turns in degrees
  """
  def __init__(self, at = [0, 0, 0], orientation = 0, theta = 45 + 180):
    self.location = np.float32(at)
    self.orientation = -1 * orientation * math.pi/180
    self.theta = theta * math.pi / 180
    self.name = NAME
    self.mesh = Mesh('path-bent.mesh', at, folder='./SimEntities/Meshes/pathbent/')
    
    line = np.float32([math.sin(self.orientation), math.cos(self.orientation), 0])
    line2 = np.float32([math.sin(self.orientation + self.theta), math.cos(self.orientation + self.theta), 0])

    widthLine = np.float32([math.cos(self.orientation), -1*math.sin(self.orientation), 0])
    widthLine2 = np.float32([math.cos(self.orientation + self.theta), -1*math.sin(self.orientation + self.theta), 0])
    
    midTheta = self.orientation - (theta - math.pi) / 2.0
    midLine = np.float32([math.sin(midTheta), math.cos(midTheta), 0])
    
    midLength = pathWidth / (2.0 * math.sin(theta/2) )
    
    p1 = self.location + pathLength/2 * line + widthLine/2 * pathWidth
    p2 = self.location + pathLength/2 * line - widthLine/2 * pathWidth
    p3 = self.location + midLength * midLine
    p4 = self.location - midLength * midLine
    p5 = self.location + pathLength/2 * line2 - widthLine2/2 * pathWidth
    p6 = self.location + pathLength/2 * line2 + widthLine2/2 * pathWidth
    
    self.points1 = [p1, p2, p3, p4]
    self.points2 = [p5, p6, p3, p4]


    self.color = (0, 0, 255)
    if DB:
      self.db = dbEntity(self.location, name = self.name)
  
  def draw(self, roboPos, COBM, camera):
    if DB:
      self.db.draw(roboPos, COBM, camera)
    pts = []
    
    for pt in self.points1:
      pts.append(np.dot(COBM, pt - roboPos))
    
    camera.drawPoly(pts, self.color)
    circ = [(pts[0][0] + pts[1][0])/2.0, (pts[0][1] + pts[1][1])/2.0, pts[0][2]]
    camera.drawCirc(circ, pathWidth/2, (0,0,255))

    pts = []
    for pt in self.points2:
      pts.append(np.dot(COBM, pt - roboPos))
    
    camera.drawPoly(pts, self.color)
    circ = [(pts[0][0] + pts[1][0])/2.0, (pts[0][1] + pts[1][1])/2.0, pts[0][2]]
    camera.drawCirc(circ, pathWidth/2, (0,0,255))
    return

  def update(self):
    pass
 
 
  def loc(self):
    return self.location  
  
  def getName(self):
    return self.name
