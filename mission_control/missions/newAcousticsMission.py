import cv2
import sw3
import numpy as np
import time
import math
import seawolf as sw

import sys
sys.path.append("./../vision/")


from Entities import buoysHough as vision


#factor for linearly converting pixels to depth in meters, aka Meters / Pixel
PIXTODEPTH = 400.0
#how far off the robot can be from being centered on the wheel
DISTANCE_ERROR = 6

class NewAcousticsMission(object):

  def __init__(self):
    self.camera = "down"
    self.name = "NewAcousticsMission"
    self.runtime = 2200
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return type(self).__name__
  
  def setup(self):
    self.time = time.time()
    sw3.SetDepth(-1).start()
    sw3.Forward(0).start()
    self.centers = []
    return
    
    
  
  def processFrame(self, frame):
    try:
      acousticsYaw = sw.var.get("Acoustics.Yaw")
      print "Acoustics yaw is", acousticsYaw
    except:
      print "Couldn't get acoustics yaw"
    
    
    return self.runtime > (time.time() - self.time)
    
  
