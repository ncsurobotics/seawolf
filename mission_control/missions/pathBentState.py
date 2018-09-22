import cv2
import sw3
import numpy as np
from util import Timer
import math

import sys
sys.path.append("../vision/")


from Entities import pathBent as vision

"""
Mission for moving along a path. Starts at the end of the path closest
to the center of the down camera. It then moves along the path.
States are:
SearchState - looking for the path
FoundState - move to the starting point of the path
FirstTurnState - turns to face the center of the path
ToCenterState - moves to the center of the path
SecondTurnState - turns to the end point of the path
ToEndState - moves to the end point of the path
"""

#time to search for path
SEARCHTIME = 60
#time to dead reckon after path is not seen
RECKONTIME = 7
#factor for linearly converting pixels to depth in meters, aka Meters / Pixel
PIXTODEPTH = 400.0
#maximum distance the center should be from a point before being considered on it
MAXDIST = 14
#maximum difference between two angles until they are treated the same
MAXANGLEDIF = 7
#how long the path has to be lost to give up
LOSTTIME = 8
"""
Sorts the start and end points of a path by seeing which point
is closest to the previous start point. Returns the sorted points
"""
def sortPoints(startPt, pts):
    pt1, pt2 = pts
    dist1 = math.sqrt( (startPt[0] - pt1[0]) ** 2 + (startPt[1] - pt1[1]) ** 2 )
    dist2 = math.sqrt( (startPt[0] - pt2[0]) ** 2 + (startPt[1] - pt2[1]) ** 2 )
    #pt1 is closer to last start pt
    if dist1 < dist2:
        return [pt1, pt2]
    else:
        return [pt2, pt1]

"""
Moves seawolf so that it centers on a point. Returns the distance
remaining in pixels.
"""
def moveTo(frame, pt):
    x,y = pt
    h,w,_  = frame.shape
    heightError = h/2 - y
    widthError= x - w/2
    sw3.Forward(heightError / PIXTODEPTH).start()
    sw3.Strafe(widthError / PIXTODEPTH).start()
    return math.sqrt(heightError ** 2 + widthError ** 2)

"""
Turns seawolf to face the angle. Adjusts the angle from
radians to degrees. Returns the angle.
"""
def turnToAngle(angle):
  angle *= 180.0 / math.pi
  print "NEW ANGLE", angle
  #gets the angle it needs to turn by
  if angle < 0:
    angleDif = abs(angle) - 90
  elif angle < 90:
    angleDif = -90 - angle
  else:
    angleDif = 270 - angle
  sw3.RelativeYaw(angleDif).start()
  return angleDif

"""
Turns seawolf to be parallel to an angle from pt1 to pt2.
Returns the angle.
"""
def turnParallelTo(pt1, pt2):
    x1,y1 = pt1
    x2,y2 = pt2
    angle = math.atan2(y2 - y1, x2 - x1)
    return turnToAngle(angle)
    

"""
Turns seawolf to face the given point.
Returns the angle to the point.
"""
def turnToPt(frame, pt):
    x,y = pt
    h,w,_  = frame.shape
    angle = math.atan2(y - h/2, x - w/2)
    return turnToAngle(angle)


class PathBentState(object):

  def __init__(self):
    self.camera = "down"
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
  
  def processFrame(self, frame):
    path = vision.ProcessFrame(frame)
    print path.found
    if path.found:
      frame = path.draw(frame)
      self.foundCounter -= 1
      if self.foundCounter <= 0:
        #closest point to center is start point
        h,w,_  = frame.shape
        pt1, pt2 = [[path.p1x, path.p1y], [path.p2x, path.p2y]]
        dist1 = math.sqrt( (w/2 - pt1[0]) ** 2 + (h/2 - pt1[1]) ** 2 )
        dist2 = math.sqrt( (w/2 - pt2[0]) ** 2 + (h/2 - pt2[1]) ** 2 )
        if dist1 < dist2:
          return FoundState(pt1, pt2)
        else:
          return FoundState(pt2, pt1)
        
    return self
  
  def cont(self):
    """ if true continue mission, false end mission"""
    return self.timer.timeLeft()


class FoundState(object):
  def __init__(self, startPt, endPt):
    #after path has not been seen for 2 secs, quit
    self.pathLost = Timer(LOSTTIME)
    self.centers = []
    self.startPt = startPt
    self.endPt = endPt
    sw3.Forward(0).start()
    
  def processFrame(self, frame):
    print "found state"
    path = vision.ProcessFrame(frame)
    if path.found:
      print "path found"
      self.pathLost.restart()
      """
      finding out where the start of the path is. This is the path
      end point closest to the center of the camera
      """
      #pt1, pt2 = path.endPoints()
      pts = [[path.p1x, path.p1y], [path.p2x, path.p2y]]
      self.startPt, self.endPt = sortPoints(self.startPt, pts)
      cx, cy = (path.cx, path.cy)
      
      if moveTo(frame, self.startPt) <= MAXDIST:
          return FirstTurnState(self.startPt, self.endPt)
      
      
    elif not self.pathLost.timeLeft():
      """if the path has been lost for too long go to path lost state"""
      return PathLostState()
    
    print "ret found"
    return self
    
  def cont(self):
    #path missions never stops while we see path
    return True

class FirstTurnState(object):
  def __init__(self, startPt, endPt):
    #after path has not been seen for 2 secs, quit
    self.pathLost = Timer(LOSTTIME)
    self.centers = []
    self.startPt = startPt
    self.endPt = endPt
    sw3.Forward(0).start()
    sw3.Strafe(0).start()
    
  def processFrame(self, frame):
    print "found state"
    path = vision.ProcessFrame(frame)
    if path.found:
      print "path found"
      self.pathLost.restart()
      """
      finding out where the start of the path is. This is the path
      end point closest to the center of the camera
      """
      #pt1, pt2 = path.endPoints()
      pts = [[path.p1x, path.p1y], [path.p2x, path.p2y]]
      self.startPt, self.endPt = sortPoints(self.startPt, pts)
      center = (path.cx, path.cy)
      angle = turnParallelTo(self.startPt, center)
      print "Angle: %d" % angle
      if abs(angle) <= MAXANGLEDIF:
          sw3.RelativeYaw(0).start()
          return ToCenterState(self.startPt, self.endPt)
      
    elif not self.pathLost.timeLeft():
      """if the path has been lost for too long go to path lost state"""
      return PathLostState()
    
    print "ret found"
    return self
    
  def cont(self):
    #path missions never stops while we see path
    return True

class ToCenterState(object):
  def __init__(self, startPt, endPt):
    #after path has not been seen for 2 secs, quit
    self.pathLost = Timer(LOSTTIME)
    self.centers = []
    self.startPt = startPt
    self.endPt = endPt
    sw3.Forward(0).start()
    
  def processFrame(self, frame):
    print "found state"
    path = vision.ProcessFrame(frame)
    if path.found:
      print "path found"
      self.pathLost.restart()
      """
      moving to the center of the path.
      """
      pts = [[path.p1x, path.p1y], [path.p2x, path.p2y]]
      self.startPt, self.endPt = sortPoints(self.startPt, pts)
      center = (path.cx, path.cy)
      
      if moveTo(frame, center) <= MAXDIST:
          return SecondTurnState(self.startPt, self.endPt)
      
      
    elif not self.pathLost.timeLeft():
      """if the path has been lost for too long go to path lost state"""
      return PathLostState()
    
    print "ret found"
    return self
    
  def cont(self):
    #path missions never stops while we see path
    return True

class SecondTurnState(object):
  def __init__(self, startPt, endPt):
    #after path has not been seen for 2 secs, quit
    self.pathLost = Timer(LOSTTIME)
    self.centers = []
    self.startPt = startPt
    self.endPt = endPt
    sw3.Forward(0).start()
    sw3.Strafe(0).start()
    
  def processFrame(self, frame):
    print "found state"
    path = vision.ProcessFrame(frame)
    if path.found:
      print "path found"
      self.pathLost.restart()
      """
      Turning to face the end point of the path.
      """
      #pt1, pt2 = path.endPoints()
      pts = [[path.p1x, path.p1y], [path.p2x, path.p2y]]
      self.startPt, self.endPt = sortPoints(self.startPt, pts)
      center = (path.cx, path.cy)
      angle = turnParallelTo(center, self.endPt)
      print "Angle: %d" % angle
      if abs(angle) <= MAXANGLEDIF:
          sw3.RelativeYaw(0).start()
          return ToEndState(self.startPt, self.endPt)
      
    elif not self.pathLost.timeLeft():
      """if the path has been lost for too long go to path lost state"""
      return PathLostState()
    
    print "ret found"
    return self
    
  def cont(self):
    #path missions never stops while we see path
    return True

class ToEndState(object):
  def __init__(self, startPt, endPt):
    #after path has not been seen for 2 secs, quit
    self.pathLost = Timer(LOSTTIME)
    self.centers = []
    self.startPt = startPt
    self.endPt = endPt
    sw3.Forward(0).start()
    self.atEnd = False
    
  def processFrame(self, frame):
    print "found state"
    path = vision.ProcessFrame(frame)
    if path.found:
      print "path found"
      self.pathLost.restart()
      """
      moving to the end of the path.
      """
      pts = [[path.p1x, path.p1y], [path.p2x, path.p2y]]
      self.startPt, self.endPt = sortPoints(self.startPt, pts)
      center = (path.cx, path.cy)
      
      if moveTo(frame, self.endPt) <= MAXDIST:
          self.atEnd = True
      
      
    elif not self.pathLost.timeLeft():
      """if the path has been lost for too long go to path lost state"""
      return PathLostState()
    
    print "ret found"
    return self
    
  def cont(self):
    #path missions never stops while we see path
    return not self.atEnd

class PathLostState(object):
  
  def __init__(self):
    self.stopTime = Timer(RECKONTIME)
  
  def processFrame(self, frame):
    return self
  
  def cont(self):
    return self.stopTime.timeLeft()
