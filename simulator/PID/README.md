PID is the module to be used to fake pid data

pid classes must implement the following methods:
  __init__()    creates object that has .update() method
  object.update()   the update method must update the pidaxis in HUB

