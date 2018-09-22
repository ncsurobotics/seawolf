import cv2
import sw3
import numpy as np
import time
from util import Timer


import sys
sys.path.append("./../vision/")


from Entities import diceContour as vision


#factor for linearly converting pixels to depth in meters, aka Meters / Pixel
PIXTODEPTH = 400.0

#time to search for dice
SEARCHTIME = 60
#time to dead reckon after dice is not seen
RECKONTIME = 7
#factor for linearly converting pixels to depth in meters, aka Meters / Pixel
PIXTODEPTH = 400.0
#maximum distance the center should be from a point before being considered on it
MAXDIST = 14
#maximum difference between two angles until they are treated the same
MAXANGLEDIF = 7
#how long the dice has to be lost to give up
LOSTTIME = 3
class DiceMS(object):

  def __init__(self):
    self.camera = "forward"
    self.name = "dicePID"
    self.runtime = 200
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return type(self).__name__
  
  def setup(self):
    sw3.SetDepth(-1).start()
    sw3.Forward(.8).start()
    self.state = SearchState()
    return
    
  def processFrame(self, frame):
    print type(self.state).__name__
    self.state = self.state.processFrame(frame)
    return self.state.cont()
    
class SearchState(object):
  def __init__(self):
    self.timer = Timer(SEARCHTIME)
    self.foundCounter = 4
    self.foundCount = 0
  
  def processFrame(self, frame):
    dice = vision.ProcessFrame(frame)
    print dice.found
    if dice.found:
      self.foundCount += 1
    if self.foundCount >= self.foundCounter:
      return FoundState()


        
    return self
  
  def cont(self):
    """ if true continue mission, false end mission"""
    return self.timer.timeLeft()


class FoundState(object):
  def __init__(self):
    #after path has not been seen for 2 secs, quit
    self.diceLost = Timer(LOSTTIME)
    self.centers = []
    self.pastDice = False
    sw3.Forward(.1).start()
  def processFrame(self, frame):
    print "found state"
    dice = vision.ProcessFrame(frame)
    if dice.found:
      print "found dice"
      self.diceLost.restart()
      (x, y, _) = dice.closestLoc(frame)
      h,w,_  = frame.shape
      
      heightError = h/2 - y
      
      print('modifying depth by: %.3f' % (heightError / PIXTODEPTH))
      sw3.RelativeDepth(heightError / PIXTODEPTH).start()
      print "x is : ", x
      widthError= x - w/2
      print "w is : ", widthError

      print('turning: %.3f' % (widthError / PIXTODEPTH))
      
      if widthError > 0:
        print "<<"
        sw3.RelativeYaw( .0001).start()
      else:
        print ">>"
        sw3.RelativeYaw( -.0001 ).start()

    #elif not self.diceLost.timeLeft():
    #  """if the dice has been lost for too long go to path lost state"""
    #  return LostState()

    if not self.diceLost.timeLeft():
      print "stopping seawolf"
      sw3.RelativeDepth(0).start()
      sw3.Strafe(0).start()
      self.pastDice = True
    
    print "ret found"
    return self
    
  def cont(self):
    #path missions never stops while we see path
    return not self.pastDice

class LostState(object):
  
  def __init__(self):
    self.stopTime = Timer(RECKONTIME)
  
  def processFrame(self, frame):
    print "lost state"
    return self
  
  def cont(self):
    return self.stopTime.timeLeft()
