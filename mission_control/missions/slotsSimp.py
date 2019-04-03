import cv2
import sw3
import numpy as np
import time


import sys
sys.path.append("../vision/")

from Entities import slots as vision

sys.path.append("../simulator/Pneumatics")
from torpedo import fireTorpedo



#factor for linearly converting pixels to degrees to turn
PIXTODEG = 70

class SlotsSimp(object):

  def __init__(self):
    self.camera = "forward"
    self.name = "SlotsSimp"
    self.runtime = 80
    fireTorpedo()
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return type(self).__name__
  
  def setup(self):
    self.time = time.time()
    return
    
    
  
  def processFrame(self, frame):
    slots = vision.ProcessFrame(frame)
    print slots.found, slots.locations
    
    if slots.found:
      frame = slots.draw(frame)
      # find how many pixels from center it is
      # strafe and depth to make biggest hole centered

    cv2.imshow(self.name, frame)
    
    
    return self.runtime > (time.time() - self.time)
    
  
