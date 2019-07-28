"""
viewSim is the module to be used to fake camera data, and broadcast on SVR
  init(locations) the setup mehtod is input a array of entities
  update(roboPos) the update method is input a 3 piece array [x, y, z] containing the location of the robot and sends out and svr frame for forward and down simulating what the camera's would see.
"""
# TODO: store render address and sim address in hub

import matplotlib.pyplot as plt
import numpy as np
import time
import math
import seawolf as sw
import svr
from Cameras import Camera
import renderCom as rc
import cv2
from bytesMailBox import BytesMailBox
import comAddresses

class ViewSimpleSim(object):
  
  
  #entities = array of entities to be seen by robot
  def __init__(self, entities = None):
    self.entities = entities
    #setting the scale factor, this means each pixel is one cm when obj is 1m away
    sf = .0017
    svr.connect()
    
    #making the down camera
    downTransform = np.float32([[1, 0, 0],
                                [0, 1, 0],
                                [0, 0, -1 * sf]])
    downCam = Camera(name = "down", transform = downTransform)
    
    #making the forward camera
    forTransform = np.float32([[1,      0, 0],
                               [ 0,      0, 1],
                               [ 0, sf * 1, 0]])
    forCam = Camera(name = "forward", transform = forTransform)

    self.mailBox = BytesMailBox(ip_and_port=comAddresses.VIEW_ADDRESS)
    
    self.cams = [downCam, forCam]
    return
  
  
  """
  sorts entities then draws them on frame, and sends frame to svr
  roboPos = position of robot
  """
  def updateViews(self, roboPos):
    rotPos = 0
    while(True):
      rotPos += .1
      data = rc.Message("ROT", [rotPos, 0]).serialize()

      self.mailBox.send(data, comAddresses.RENDER_ADDRESS)
      img_bytes = self.mailBox.receive()[0]

      frame = cv2.imdecode(np.fromstring(img_bytes, dtype=np.uint8), 1)

      # Display the resulting frame
      cv2.imshow('frame', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.destroyAllWindows()

    if self.entities == None:
      return
    self.roboPos = np.float32(roboPos)
    self.entities = sorted(self.entities, key = self.sort, reverse = True)
    
    
    """
    this section changes the cordinate system of the object to one where the origin is the robot
    and the axis match the heading of the robot. aka y is straight ahead of the robot
    """
    # getting robot direction and turning it to radians
    heading = -1 * sw.var.get("SEA.Yaw") * math.pi / 180.0 
    #creating the Rotation Matrix
    R = np.array([[-1* math.cos(heading),  math.sin(heading), 0],
                  [math.sin(heading),      math.cos(heading), 0],
                  [                0,                 0     , 1]], np.float32)
    for cam in self.cams:
      cam.newFrame()
      for ent in self.entities:
        ent.draw(roboPos, R, cam)
      cam.show()
    
    return
  
  #used by built in sort() to sort entities based on distance to robot, makes it so that things that are closer are drawn last, and such overlap things that are farther away.
  def sort(self, obj):
    return np.sum((obj.loc() - self.roboPos)**2)
  
