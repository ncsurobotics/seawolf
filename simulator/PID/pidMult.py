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

#function for adding noise to the pid
#noise will be modified/normalized by time between updates by update function
def noise():
  return random.gauss(0, .03)
  
def depthNoise():
  return random.gauss(0, .001)

class axis(object):
  """
  axis to be updated by PID
  """
  
  def __init__(self, actual, desired, updateRate, noise):
    self.actual = actual
    self.desired = desired
    self.updateRate = updateRate
    self.noise = noise
  
  def updateHeading(self, td):
    updateValue = self.updateRate * td
    dbPrint("updateVal: %.4f" % (updateValue))
    val = sw.var.get(self.actual) 
    desired = sw.var.get(self.desired)
    dbPrint("%6s: val: %6.2f des: %6.f" % (self.actual, val, desired))
    diff = desired - val
    """new """
    diff = diff % 360
    if diff < 180 and diff > updateValue:
      val += updateValue * diff/abs(diff)
    elif diff < updateValue:
      val = desired
    else:
      val -= updateValue * diff/abs(diff)
      
    val+= self.noise() * td
    if val < -180:
      val = 360 + val
    if val > 180:
      val = val - 360
    sw.var.set(self.actual, val)
      

class pid(object):
    
  def __init__(self):
    self.prevTime = time.time()
    #rate of update deg/s 
    updateRate = 10
    self.axis = [axis("SEA.Pitch", "PitchPID.Heading", updateRate, noise),
                 axis("SEA.Yaw"  , "YawPID.Heading", 20.0, noise),
                 axis("SEA.Roll" , "RollPID.Heading", updateRate, noise),
                 axis("Depth"    , "DepthPID.Heading", .1, depthNoise)
                ]
  
  def updateHeading(self):
    # sw.var.set(name, value)
    # sw.var.get(name)
    timeDiff = time.time() - self.prevTime
    for axis in self.axis:
      axis.updateHeading(timeDiff)
      
    self.prevTime = time.time()  
    dbPrint("////////////////")
    sw.notify.send("UPDATED", "IMU")
    return

      
       
    
