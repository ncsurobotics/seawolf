import cv2
import sw3
import numpy as np
import time


import sys
sys.path.append("./../vision/")


from Entities import buoysHough as vision


#factor for linearly converting pixels to depth in meters, aka Meters / Pixel
PIXTODEPTH = 400.0

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
    sw3.Forward(0).start()
    self.centers = []
    return
    
    
  
  def processFrame(self, frame):
    buoys = vision.ProcessFrame(frame)
    
    if buoys.found:
      (x, y) = buoys.loc()
      h,w,_  = frame.shape
      
      heightError = h/2 - y
      print('modifying depth by: %.3f' % (heightError / PIXTODEPTH))
      sw3.RelativeDepth(heightError / PIXTODEPTH).start()
      
      widthError= x - w/2
      print('setting strafe to: %.3f' % (widthError / PIXTODEPTH))
      sw3.Strafe(widthError / PIXTODEPTH).start()
      
      
      
      
    
    
    
    
    return self.runtime > (time.time() - self.time)
    
  
