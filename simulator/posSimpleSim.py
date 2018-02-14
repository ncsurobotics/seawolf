"""
posSim is the module to be used to fake position of data
posSim mus implement the following methods:
  setup()   this mehtod returns an object that has .update() and .pos() method
  object.update() this method updates the position of seawolf based on locally stored prev value and values in hub
  object.pos() returns 3 value array [x, y, z] containings current location of seawolf
"""
import seawolf as sw
import math
import numpy as np
import matplotlib.pyplot as plt
import time

debug = False
def dbPrint(msg):
  if debug:
    print "posSim: " +  msg
  return

#location is 3 piece array containing start location [x, y, z]
#axis limits is a 1 by 2 array containing limit for x and y axis
#objects = array of entites to be seen to plot in chart
class seawolfPos(object):
  def __init__(self, location = [0, 0, 0], axis = [-10, 10], objects = {}):
    #location is in meters [x, y, z]
    self.position = location
    #speed of robot in m/s when port & startboard = 1 aka max power, distance travel is self.maxSpeed*time*meanOfPort&StarPower
    self.maxSpeed = .5
    #previous update time
    self.prevTime = time.time()
    
    #calling the function that sets up the view of the robot
    #there is a current bug when attempting to resize the window
    self.setupView(axis, objects)
    return 

  def setupView(self, axisLimits, objects):
    self.fig = plt.figure()
    self.ax = self.fig.add_subplot(111)

    # some X and Y data 
    self.Xlocs = [0]
    self.Ylocs = [0]

    self.li, = self.ax.plot(self.Xlocs, self.Ylocs, 'bo')
    
    #setting label
    self.ax.set_ylabel("Y axis in Meters")
    self.ax.set_xlabel("X axis in Meters")
    self.ax.set_title("X-Y position of Robot")
    
    # writing location of obj in water
    # currently just filler
    for obj in objects:
      pos = obj.loc()
      name = obj.getName()
      self.ax.text(pos[0], pos[1], name[0], style='italic',
        bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    
    
    #setting up view 
    self.ax.relim()
    self.ax.set_ylim(axisLimits)
    self.ax.set_xlim(axisLimits)
    self.ax.autoscale_view(True,True,True)
    self.ax.grid(b = True, axis = 'both', color = 'k')
    self.fig.canvas.draw()
    plt.show(block=False)
  
  
  def updatePosition(self):
    tDiff = time.time() - self.prevTime
    self.prevTime = time.time()
    portPower = sw.var.get("Port")
    starPower = sw.var.get("Star")
    power = (portPower + starPower)/2.0
    dist = power * self.maxSpeed * tDiff
    direction = sw.var.get("SEA.Yaw")
    
    #y val is cos bc angle is relative to y axis because y axis is forward
    self.position[0] += -1 * dist * math.sin(math.pi/180 * direction)
    self.position[1] += dist * math.cos(math.pi/180 * direction)
    self.position[2] = sw.var.get("Depth")
    dbPrint("roboPos: %d %d %d\t tdiff = %4.3f dist= %4.3f" % (self.position[0], self.position[1], self.position[2], tDiff, dist))
    
    #graphing the location
    roboPos = self.pos()
    self.Xlocs.append(roboPos[0])
    self.Ylocs.append(roboPos[1])
    # set the new data
    self.li.set_ydata(self.Ylocs)
    self.li.set_xdata(self.Xlocs)
    self.fig.canvas.draw()
    
    return
  
  def pos(self):
    return self.position
    
