import cv2
import numpy as np
import time
import seawolf as sw
import sw3

class WaitForGo(object):

  def __init__(self):
    self.camera = "forward"
    self.name = "WaitForGo"
    return
  
  def getCamera(self):
    return self.camera
  
  def getName(self):
    return self.name
  
  def setup(self):
    return
  
  def processFrame(self, frame):
    sw.notify.filter(sw.FILTER_ACTION, "EVENT")
    sw.notify.get()
    sw.var.set("MissionReset", 0)
    sw3.RelativeYaw(0).sart()
    #this assumes that roll and pitch will always be set to 0
    
    
