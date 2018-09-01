import cv2
import numpy as np
import time

class Dummy(object):

  def __init__(self):
    self.camera = "forward"
    self.name = "Dummy"
    self.runtime = 10
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return self.name
  
  def setup(self):
    self.time = time.time()
    return
  
  def processFrame(self, frame):
    cv2.imshow(self.name, frame)
    
    cv2.waitKey(1)
    return self.runtime > (time.time() - self.time)
    
  
