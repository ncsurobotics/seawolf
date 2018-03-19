import cv2
import sw3
import numpy as np
import time


import sys
sys.path.append("./../vision2/")


from Entities import pathDist as vision




class PathSimp(object):

  def __init__(self):
    self.camera = "down"
    self.name = "DownSimp"
    self.runtime = 80
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
    path = vision.ProcessFrame(frame)
    
    print path.found
    
    
    if path.found:
      frame = path.draw(frame)
      
      """
			finding out how many pixels from the center the gate is
			the center obj of the gate is the number or pixels over the gate is. 
			Subtracting the middle pixel index from it returns a pos value if the gate is to left
			and pos value if the gate is to the right
      """
      angle = path.orientation
      print("got angle %d" % angle)
      self.centers.insert(0, angle)
      count = 0
      centers = 0
      for i in self.centers:
        count +=1
        centers += i
        if count > 10:
          break
      if count > 10:
        self.centers.pop() 
      print(len(self.centers))  
      center = float(centers)/count
      print(center)
      sw3.RelativeYaw(-1 * center ).start()
      
		
    return self.runtime > (time.time() - self.time)
    
  
