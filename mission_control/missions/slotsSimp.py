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
      # strafe and depth to make smallest hole centered
      if len(slots.locations) >= 2:
        minArea = slots.locations[0][2] * slots.locations[0][3] #first length * width
        minIdx = 0
        idx = 0
        for x, y, w, h in slots.locations:
          area = w * h
          area = x
          if area < minArea:
            minIdx = idx
            minArea = x
            #minArea = area
          idx += 1
        x, y, w, h = slots.locations[minIdx]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,250,250),5)
        minLocX, minLocY = x + w / 2, y + h / 2
        print "MIN LOC: ", minLocX, minLocY
        h,w,_  = frame.shape
        errorY = h/2 - minLocY
        errorX = minLocX - w/2
        print "Error: ", errorX, errorY
        print('setting strafe to: %.3f' % (errorX / PIXTODEG))
        sw3.Strafe(errorX / PIXTODEG).start()
        #sw3.RelativeYaw(errorX / (PIXTODEG * 10) ).start()
        try:
          sw3.RelativeDepth(errorY / abs(errorY)).start()
        except Exception as e:
          pass
        # once centered long enough, shoot torpedo
         

    cv2.imshow(self.name, frame)
    
    
    return self.runtime > (time.time() - self.time)
    
  
