import cv2
import sw3
import numpy as np
import time


import sys
sys.path.append("./../vision2/")


from Entities import buoysHough as vision


#factor for linearly converting pixels to degrees to turn
PIXTODEG = 70

class BuoysPID(object):

  def __init__(self):
    self.camera = "forward"
    self.name = "BuoySimp"
    self.runtime = 200
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return type(self).__name__
  
  def setup(self):
    self.time = time.time()
    sw3.SetDepth(-1).start()
    sw3.Forward(.3).start()
    self.centers = []
    return
    
    
  
  def processFrame(self, frame):
    buoys = vision.ProcessFrame(frame)
    
    print buoys.found
    
    
    
    
    return self.runtime > (time.time() - self.time)
    
  
