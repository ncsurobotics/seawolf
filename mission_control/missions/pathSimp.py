import cv2
import sw3
import numpy as np
import time


import sys
sys.path.append("./../vision/")


from Entities import pathDist as vision




class PathSimp(object):

  def __init__(self):
    self.camera = "down"
    self.name = "DownSimp"
    self.runtime = 30
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return type(self).__name__
  
  def setup(self):
    self.time = time.time()
    sw3.SetDepth(-1).start()
    sw3.Forward(.5).start()
    self.centers = []
    return
    
    
  
  def processFrame(self, frame):
    path = vision.ProcessFrame(frame)
    
    print path.found
    
    
    if path.found:
      frame = path.draw(frame)
      print("got angle %d" % path.orientation)
      sw3.RelativeYaw( path.orientation ).start()
      
		
    return self.runtime > (time.time() - self.time)
    
  
