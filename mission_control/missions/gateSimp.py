import cv2
import sw3
import numpy as np
import time


import sys
sys.path.append("../vision/")


from Entities import gateHoughProb as vision


#factor for linearly converting pixels to degrees to turn
PIXTODEG = 70

class GateSimp(object):

  def __init__(self):
    self.camera = "forward"
    self.name = "GateSimp"
    self.runtime = 80
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
    gate = vision.ProcessFrame(frame)
    
    print gate.found
    
    
    if gate.found:
      frame = gate.draw(frame)
      
      """
			finding out how many pixels from the center the gate is
			the center obj of the gate is the number or pixels over the gate is. 
			Subtracting the middle pixel index from it returns a pos value if the gate is to left
			and pos value if the gate is to the right
      """
      _, w, _ = frame.shape
      center = w/2.0 - gate.cp
      print("got center %d" % center)
      self.centers.insert(0, center)
      
      centers = 0
      for i in self.centers:
        centers += i
          
      center = float(centers)/len(self.centers)
      print(center)
      sw3.RelativeYaw(center / PIXTODEG).start()
      
			
			
    cv2.imshow(self.name, frame)
    
    
    return self.runtime > (time.time() - self.time)
    
  
