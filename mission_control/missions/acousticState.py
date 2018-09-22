import cv2
import sw3
import numpy as np
import seawolf as sw

import sys
sys.path.append("../vision/")


from Entities import gateDist as vision

#amount of pixels to be off by to initate turn, aka filter for noise
PITCHCUT = 15
PITCHSTP = 10

class AcousticState(object):

  def __init__(self):
    self.camera = "forward"
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return type(self).__name__
  
  def setup(self):
    sw3.SetDepth(-1).start()
    sw3.Forward(.4).start()
    self.state = YawState()
    return
    
  def processFrame(self, frame):
    print type(self.state).__name__
    self.state = self.state.processFrame(frame)
    return self.state.cont()
    

class YawState(object):
  def __init__(self):
    #initiating yaw and pitch values with impossible values
    self.yaw = 361
    self.pitch = 361
  
  def processFrame(self, frame):
    yaw = sw.var.get("Acoustics.Yaw")
    pitch = abs(sw.var.get("Acoustics.Pitch"))
    print("Yaw: %4.2f, Pitch %4.2f" % (yaw, pitch))
    if yaw != self.yaw or pitch != self.pitch:
      self.yaw = yaw
      self.pitch = pitch
      if pitch >= PITCHCUT:
        sw3.RelativeYaw(yaw).start()
      else:
        return PitchState(pitch)
    return self
    
    
  def cont(self):
    """ if true continue mission, false end mission"""
    return True


class PitchState(object):
  def __init__(self, pitch):
    self.pitch = pitch
    
  def processFrame(self, frame):
    pitch = abs(sw.var.get("Acoustics.Pitch"))
    if pitch != self.pitch:
      self.pitch = pitch
      if pitch <= PITCHSTP:
        return StopState()
    return self
    
  def cont(self):
    return True
			

class StopState(object):
  
  def __init__(self):
    sw3.Forward(0).start()
    self.c = 10
  
  def processFrame(self, frame):
    return self
  
  def cont(self):
    if self.c > 0:
      self.c-=1
      print "on pinger"
      return True
    return 
    
    
    
    
  
