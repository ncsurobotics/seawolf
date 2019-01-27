"""
viewSim is the module to be used to fake camera data, and broadcast on SVR
  init(locations) the setup mehtod is input a array of entities
  update(roboPos) the update method is input a 3 piece array [x, y, z] containing the location of the robot and sends out and svr frame for forward and down simulating what the camera's would see.
"""


import matplotlib.pyplot as plt
import numpy as np
import time
import math
import seawolf as sw
import srv
from Cameras.camera import Cam



class ViewSimpleSim(object):
  
  
  #entities = array of entities to be seen by robot
  def __init__(self, entities = None):
    self.entities = entities

    self.meshes = []
    for e in entities:
      if hasattr(e, 'mesh'):
        self.meshes.append(e.mesh)
    #svr.connect()
    

    forCam = Cam(name="forward")
    downCam = Cam(name="down", rot_offset=(math.pi/2,0))
    
    self.cams = [downCam, forCam]
    return
  
  
  """
  sorts entities then draws them on frame, and sends frame to svr
  roboPos = position of robot
  """ 
  def updateViews(self, roboPos):
    if self.entities == None:
      return
    for cam in self.cams:
      # cam located at where robot is
      x,y,z = roboPos[:]
      cam.pos = x,-z,y
      # swap y and z in cam.pos to convert simulator coordinates to graphics coordinates
      # the vertical axis must be negated as well
      #temp = cam.pos[1]
      #cam.pos[1] = cam.pos[2]
      #cam.pos[2] = temp
      #print "-" * 20, cam.pos
      #cam.pos[1] = -1
      # have camera yaw and pitch be same as robot's
      cam.rot[1] = -1 * sw.var.get("SEA.Yaw") * math.pi / 180.0
      cam.rot[0] = sw.var.get("SEA.Pitch") * math.pi / 180.0
      # draw and display the frame
      cam.draw(self.meshes)
      cam.show()
    
    return