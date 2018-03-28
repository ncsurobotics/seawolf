Pos is the module to be used to fake position of data
pos classes must implement the following methods:
  this is an object that has .update() and .pos() method
  init(pos) 1 by 3 array containg [x, y, z] start pos of robot
  object.update() this method updates the position of seawolf based on locally stored prev value and values in hub
  object.pos() returns 3 value array [x, y, z] containings current location of seawolf

