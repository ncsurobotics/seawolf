import cv2
import sw3
import numpy as np
import math

from util import Timer

import sys
sys.path.append("./../vision/")



#factor for linearly converting pixels to depth in meters, aka Meters / Pixel
PIXTODEPTH = 400.0
#how far off the robot can be from being centered on the wheel, in pixels
DISTANCE_ERROR = 18

""" Uses buoysHough to detect circle in image """
from Entities import wheelHough as vision

#time to search for wheel in secondsF
SEARCHTIME = 50
#error to be off from center in pixels

class WheelState(object):

  def __init__(self):
    self.camera = "down"
    self.name = "WheelMS"
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return type(self).__name__
  
  def setup(self):
    sw3.Forward(.8).start()
    self.state = SearchState()
    return
    
  def processFrame(self, frame):
    print type(self.state).__name__
    self.state = self.state.processFrame(frame)
    return self.state.cont()
 
"""
Robot moves forward until it sees the wheel consistently
or runs out of search time.
"""
class SearchState(object):
  def __init__(self):
    self.timer = Timer(SEARCHTIME)
    #number of times to see wheel before going to next state
    self.foundCounter = 6
  
  def processFrame(self, frame):
    wheel = vision.ProcessFrame(frame)
    print wheel.found
    if wheel.found:
      #maybe kill this line
      frame = wheel.draw(frame)
      
      self.foundCounter -= 1
      if self.foundCounter <= 0:
        return FoundState()
    return self
  
  def cont(self):
    """ if true continue mission, false end mission"""
    return self.timer.timeLeft()

"""
Wheel has been found. Robot moves to hover over the wheel.
"""
class FoundState(object):
  def __init__(self):
    #after wheel has not been seen for 8 secs, quit
    self.wheelLost = Timer(8)
    #timer for being centered on the wheel
    self.centeredTimer = Timer(2)
    
  def processFrame(self, frame):
    print "found state"
    wheel = vision.ProcessFrame(frame)
    if wheel.found:
      print "wheel found"
      self.wheelLost.restart()
      """
            finding out how many pixels from center of down camera the wheel is
			Finds difference between wheel's center in screen space and center
            of the screen, then moves robot to cover that distance.
      """
      (x, y) = wheel.loc()
      h,w,_  = frame.shape
      
      heightError = h/2 - y
      print('Height error: %.3f' % heightError)
      widthError= x - w/2
      print('Width error: %.3f' % widthError)

      distance = math.sqrt(heightError ** 2 + widthError ** 2)
      #excluding depth
      print("Distance from center of wheel: %.3f" % distance)
      """
      Robot moves to center itself on the wheel until it has been centered
      within DISTANCE_ERROR's threshhold long enough.
      """
      print('moving forward by: %.3f' % (heightError / PIXTODEPTH))
      sw3.Forward(heightError / PIXTODEPTH).start()
        
      print('setting strafe to: %.3f' % (widthError / PIXTODEPTH))
      sw3.Strafe(widthError / PIXTODEPTH).start()

      """Restart the timer for being centered on the wheel"""
      if not distance <= DISTANCE_ERROR:
        self.centeredTimer.restart()
        
      if not self.centeredTimer.timeLeft():
          sw3.Forward(0).start()
          sw3.Strafe(0).start()
          return CenteredState()
    elif not self.wheelLost.timeLeft():
      """if the wheel has been lost for too long go to lost state"""
      return WheelLostState()
    
    print "ret found"
    return self
    
  def cont(self):
    #wheel missions never stops in this state, only in lost or centered states
    return True
			
"""
Error state for if the wheel cannot be found for some reason.
"""
class WheelLostState(object):
  
  def __init__(self):
    pass
  
  def processFrame(self, frame):
    return self
  
  def cont(self):
    print "Wheel was lost. Failure."
    return False
"""
State for when robot is centered on the wheel.
Will eventually drop golf balls here.
"""
class CenteredState(object):
  def __init__(self):
    pass
  def processFrame(self, frame):
    return self
  def cont(self):
    print "Centered on wheel. Success."
    return False
