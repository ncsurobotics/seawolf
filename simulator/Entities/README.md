Entities are the things seawofl is looking for in the water.
All enites must have the follwing things


DB = True/False
  DB is the debug variable, if db is set to true, then a graph will appear showing the x(red) and y(green) axis of the robot relative to the ent. On the bottom of the readme there are instructions of how to use the dbEntity


NAME = string
  NAME is the constant for the name of the ent


loc(self)
  this method returns a 1 by 3 np.float32 array containg the centerpoint of the obj. Usually the first input into the init is the location of the ent.
  
  
draw(self, roboPos, COBM, camera):
  this method is in charge of drawing the ent onto the camera frame. 
  roboPos = 1 by 3 np.float32 array  containing the position of the robot in meters
  COBM = 3by3 np.float32 3 by 3 matrix to transform the point from standar cordinate system to one where the robots forward is +y, robot's right is +x, currently nothing is done for pitch and roll
  camera = camera obj from Camera, ent's and the camera are highly linked!!
 
 
getName(self)
  returns the NAME of the ent


SETTING UP THE DEBUGGING
the dbEntity is made by passing it the location and name of the ent
the draw function of the ent should call the draw function of the dbEnt
each ent has on dbEnt 
