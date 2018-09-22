import cv2
import sw3
import numpy as np
from util import Timer

import sys
sys.path.append("../vision/")


from Entities import pathDist as vision



#time to search for gate
SEARCHTIME = 60
#time to dead reckon after gate is not seen
RECKONTIME = 7

class PathState(object):

  def __init__(self):
    self.camera = "down"
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return type(self).__name__
  
  def setup(self):
    sw3.SetDepth(-1).start()
    sw3.Forward(.8 ).start()
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
  
  def processFrame(self, frame):
    path = vision.ProcessFrame(frame)
    print path.found
    if path.found:
      frame = path.draw(frame)
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
    self.pathLost = Timer(2)
    self.centers = []
    sw3.Forward(.3 ).start()
    
  def processFrame(self, frame):
    print "found state"
    path = vision.ProcessFrame(frame)
    if path.found:
      print "path found"
      self.pathLost.restart()
      """
			finding out how many pixels from the center the gate is
			the center obj of the gate is the number or pixels over the gate is. 
			Subtracting the middle pixel index from it returns a pos value if the gate is to left
			and pos value if the gate is to the right
      """
      print("got direction %d" % path.orientation)
      
    
      sw3.RelativeYaw(path.orientation).start()
    elif not self.pathLost.timeLeft():
      """if the gate has been lost for too long go to gate lost state"""
      return PathLostState()
    
    print "ret found"
    return self
    
  def cont(self):
    #gate missions never stops while we see gate
    return True
			

class PathLostState(object):
  
  def __init__(self):
    self.stopTime = Timer(RECKONTIME)
  
  def processFrame(self, frame):
    return self
  
  def cont(self):
    return self.stopTime.timeLeft()
    
    
    
    
  
