"""
for now on seawolf wil have the following axis, and move the following ways:
    x axis is left to right where right is positive X
    y axis is forward and back where forward is positive Y
    z axis is up and down where up is positive
    yaw follows the right hand rule, positive increase in yaw value means robot turns left
    pitch follows the right hand rule, positive increase in pitch value means robot aims up
    roll follows the right hand rule, positive increas in roll value means robot leans left
In the simulator the followings units are used:
    for position/distance values are in decimeters
    for direction/angles values are in degrees
"""


"""
pidSim is the module to be used to fake pid data
pidSim must implement the following methods:
  setup()    this method returns an object that has .update() method
  object.update()   the update method must update the SEA.heading vals in hub
"""
import random
import time
import seawolf as sw

debug = False
def dbPrint(msg):
  if debug:
    print "pidSim: " + msg

class pid(object):
    
  def __init__(self):
    self.prevTime = time.time()
    #rate of update deg/s 
    self.updateRate = 10
    self.axis = [("SEA.Pitch", "PitchPID.Heading"),
                 ("SEA.Yaw"  , "YawPID.Heading"),
                 ("SEA.Roll" , "RollPID.Heading"),
                 ("Depth"    , "DepthPID.Heading")
                ]
 
  #function for adding noise to the pid
  #noise will be modified/normalized by time between updates by update function
  def noise(self):
    return 0 #random.gauss(0, 1)
  
  def updateHeading(self):
    # sw.var.set(name, value)
    # sw.var.get(name)
    timeDiff = time.time() - self.prevTime
    updateValue = self.updateRate * timeDiff 
    dbPrint("updateVal: %.4f" % (updateValue))
    for heading, des in self.axis:
      val = sw.var.get(heading) 
      desired = sw.var.get(des)
      dbPrint("%6s: val: %6.2f des: %6.f" % (heading, val, desired))
      diff = desired - val
      """new """
      diff = diff % 360
      if diff < 180 and diff > updateValue:
        val += updateValue * diff/abs(diff)
      elif diff < updateValue:
        val = desired
      else:
        val -= updateValue * diff/abs(diff)
      
      #end new
      
      """
      if abs(diff) > .001:
        diffC = abs(diff) % 180* abs(diff)/diff
        if abs(diffC) < abs(diff):
          diffC *= -1
        if abs(diffC) > updateValue and diff != 0:
          val += updateValue * abs(diffC)/diffC
        else:
          val = desired
      """
      val+= self.noise() * timeDiff
      
      if val < -180:
        val = 360 + val
      if val > 180:
        val = val - 360
      
      self.prevTime = time.time()
      sw.var.set(heading, val)
      
      
      
    dbPrint("////////////////")
    sw.notify.send("UPDATED", "IMU")
    return

      
       
    
