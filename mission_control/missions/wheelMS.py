import cv2
import sw3
import numpy as np
import time
import math

import sys
sys.path.append("./../vision/")


from Entities import buoysHough as vision


#factor for linearly converting pixels to depth in meters, aka Meters / Pixel
PIXTODEPTH = 400.0
#how far off the robot can be from being centered on the wheel
DISTANCE_ERROR = 6

class WheelMS(object):

  def __init__(self):
    self.camera = "down"
    self.name = "RouletteWheel"
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
    buoys = vision.ProcessFrame(frame)
    
    if buoys.found:
      print "BUOYS found -------------------------------------------------"
      (x, y) = buoys.loc()
      h,w,_  = frame.shape
      
      heightError = h/2 - y
      print('Height error: %.3f' % heightError)
      widthError= x - w/2
      print('Width error: %.3f' % widthError)

      distance = math.sqrt(heightError ** 2 + widthError ** 2)
      #excluding depth
      print("Distance from center of wheel: %.3f" % distance)

      if distance <= DISTANCE_ERROR:
        print("Centered on wheel. Halting.")
        sw3.Forward(0).start()
        sw3.Strafe(0).start()
        #drop balls

      else:

        print('modifying depth by: %.3f' % (heightError / PIXTODEPTH))
        sw3.Forward(heightError / PIXTODEPTH).start()
        
        print('setting strafe to: %.3f' % (widthError / PIXTODEPTH))
        sw3.Strafe(widthError / PIXTODEPTH).start()
      
      
      
      
    
    
    
    
    return self.runtime > (time.time() - self.time)
    
  
