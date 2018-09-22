import cv2
import sw3
import numpy as np
from util import Timer

import sys
sys.path.append("../vision/")


from Entities import gateHoughProb as vision

#amount of pixels to be off by to initate turn, aka filter for noise
SIGPIX = 15
#factor for linearly converting pixels to degrees to turn
PIXTODEG = 70
#time to search for gate
SEARCHTIME = 50
#time to dead reckon after gate is not seen
RECKONTIME = 7

class GateState(object):

  def __init__(self):
    self.camera = "forward"
    self.name = "GateSimp"
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
    #number of times to see gate before going to next state
    self.foundCounter = 6
  
  def processFrame(self, frame):
    gate = vision.ProcessFrame(frame)
    print gate.found
    if gate.found:
      frame = gate.draw(frame)
      self.foundCounter -= 1
      if self.foundCounter <= 0:
        return FoundState()
    return self
  
  def cont(self):
    """ if true continue mission, false end mission"""
    return self.timer.timeLeft()


class FoundState(object):
  def __init__(self):
    #after gate has not been seen for 2 secs, quit
    self.gateLost = Timer(2)
    self.centers = []
    
  def processFrame(self, frame):
    print "found state"
    gate = vision.ProcessFrame(frame)
    if gate.found:
      print "gate found"
      self.gateLost.restart()
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
      print self.centers
      if len(self.centers) > 10:
        self.centers.pop()
      print self.centers
      #if less than set difference ignore it
      center = center if center > SIGPIX else 0
      sw3.RelativeYaw(center / PIXTODEG).start()
    elif not self.gateLost.timeLeft():
      """if the gate has been lost for too long go to gate lost state"""
      return GateLostState()
    
    print "ret found"
    return self
    
  def cont(self):
    #gate missions never stops while we see gate
    return True
			

class GateLostState(object):
  
  def __init__(self):
    self.stopTime = Timer(RECKONTIME)
  
  def processFrame(self, frame):
    return self
  
  def cont(self):
    return self.stopTime.timeLeft()
    
    
    
    
  
