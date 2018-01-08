"""
this entity is used for debugging
it plots the location of the robot, the path the robot would take to find it and the axis of the robot
the draw() function just updates the graph, and returns the same frame that was input
""" 

import math
import numpy as np
import matplotlib.pyplot as plt


class dbEntity(object):
  """
  location = [x, y, z] in meters, position of obj in sim world
  """
  def __init__(self, location, name="db"):
    self.name = name
    self.location = np.array(location, np.float32)
    self.setupView()
  
  """
  this function handles the drawing of the drawing of an item onto the frame
  roboPos = np 1,3 array containing x,y,z pos of robot
  COBM = np 3,3 array containing the matrix to change the axis to one that follows the current heading of the robot
  frame = np x,x,3 array containing the frame to draw the object onto
  """
  def draw(self, roboPos, COBM, camera):
    curPos = self.location - roboPos
    basis = np.dot(COBM, curPos)
    
    yPx = roboPos[0] + basis[1] * COBM[1][0]
    yPy = roboPos[1] + basis[1] * COBM[1][1]
    self.yV.set_xdata([roboPos[0],  yPx])
    self.yV.set_ydata([roboPos[1],  yPy])
    
    xPx = yPx + basis[0] * COBM[0][0]
    xPy = yPy + basis[0] * COBM[0][1]
    self.xV.set_xdata([yPx, xPx])
    self.xV.set_ydata([yPy, xPy])
    
    self.li.set_xdata([roboPos[0]])
    self.li.set_ydata([roboPos[1]])
    
    #self.ax.plot(roboPos[0], roboPos[1], 'bo') this add keeping array has eq result but don't know whats more efficient 
    self.fig.canvas.draw()
    
  def loc(self):
    return self.location
     
  #need method for updating axis limits
  def setupView(self, axisLimits = [-10, 10]):
    self.fig = plt.figure()
    self.ax = self.fig.add_subplot(111)

    #li is the line that shows the robots position
    self.li, = self.ax.plot([0], [0], 'bo')
    #xV shows the x vector for the robot
    self.xV, = self.ax.plot([0], [0], 'r')
    #yV shows the y vector for the robot
    self.yV, = self.ax.plot([0], [0], 'g')
    
    #setting label
    self.ax.set_ylabel("Y axis in Meters")
    self.ax.set_xlabel("X axis in Meters")
    self.ax.set_title("Debug View: " + self.name)
    
    # writing location of obj in water
    self.ax.text(self.location[0], self.location[1], self.name[0], style='italic',
        bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    
    
    #setting up view 
    self.ax.relim()
    self.ax.set_ylim(axisLimits)
    self.ax.set_xlim(axisLimits)
    self.ax.autoscale_view(True,True,True)
    self.ax.grid(b = True, axis = 'both', color = 'k')
    self.fig.canvas.draw()
    plt.show(block=False)
