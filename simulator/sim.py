"""
for now on seawolf wil have the following axis, and move the following ways:
    x axis is left to right where right is positive X
    y axis is forward and back where forward is positive Y
    z axis is up and down where up is positive
    yaw follows the right hand rule, positive increase in yaw value means robot turns left
    pitch follows the right hand rule, positive increase in pitch value means robot aims up
    roll follows the right hand rule, positive increas in roll value means robot leans right
In the simulator the followings units are used:
    for position/distance values are in meters
    for direction/angles values are in degrees
    for time secconds are used
"""

import seawolf as sw


"""
pidSim is the module to be used to fake pid data
pidSim must implement the following methods:
  __init__()    creates object that has .update() method
  object.update()   the update method must update the pidaxis in HUB
"""
from pidSimpleSim import pid as pidSim


"""
posSim is the module to be used to fake position of data
posSim mus implement the following methods:
  this is an object that has .update() and .pos() method
  init(pos) 1 by 3 array containg [x, y, z] start pos of robot
  object.update() this method updates the position of seawolf based on locally stored prev value and values in hub
  object.pos() returns 3 value array [x, y, z] containings current location of seawolf
"""
from posSimpleSim import seawolfPos as posSim

"""
viewSim is object module to be used to fake camera data, and broadcast on SVR
  init(locations) the setup mehtod is input array with the entities in the water. documentation on what constitutes an entity object is in the Entities folder.
  update(roboPos) the update method is input a 3 piece array [x, y, z] containing the location of the robot and sends out and svr frame for forward and down simulating what the camera's would see. 
"""
from viewSimpleSim import ViewSimpleSim as viewSim


from Entities import entities

"""
array to be used for placing objects in water
rember that the location is center point of element
elements must be an Entity, look at entities folder __init__ for available
"""
def setup():
  return [
          entities["Gate"]([0, 7, -1]),
          entities["Path"]([0, 0, -5]),
          entities["Bouy"]([-1, 10, -1], color = (255, 0, 0)),
          entities["Bouy"]([0, 10, -1], color = (0, 0, 255)), 
          entities["Bouy"]([1, 10, -1], color = (0, 255, 0)),
          entities["Hedge"]([0, 19,-1]),
          entities["Path"]([0, 15, -5])
         ]

def main():
  #connecting to hub
  sw.loadConfig("../conf/seawolf.conf")
  sw.init("Simulator : Main")
  objects = setup()
  pid = pidSim()
  robo = posSim(location = [0, 0, 0], axis = [-20, 20], objects= objects)
  view= viewSim(objects)
  while True:
    pid.updateHeading()
    robo.updatePosition()
    view.updateViews(robo.pos())

if __name__ == "__main__":
  main()
