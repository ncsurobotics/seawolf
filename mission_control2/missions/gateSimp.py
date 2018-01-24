import cv2
import sw3
import numpy as np
import time


import sys
sys.path.append("./../vision2/")


from Entities import gateHoughProb as vision



class GateSimp(object):

  def __init__(self):
    self.camera = "forward"
    self.name = "GateSimp"
    self.runtime = 50
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return self.name
  
  def setup(self):
    self.time = time.time()
    sw3.SetDepth(-1).start()
    
    return
    
    
  
  def processFrame(self, frame):
    visObj = vision.ProcessFrame(frame)
    sw3.Forward(.3).start()
    
    frame = visObj.draw(frame)
    cv2.imshow(self.name, frame)
    
    
    cv2.waitKey(1)
    return self.runtime > (time.time() - self.time)
    
  
