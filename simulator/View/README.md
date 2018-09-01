the goal of the view module is to be used to fake camera data, and broadcast on SVR
The main object in this module to be used by the sim is:
  init(locations) the setup mehtod is input array with the entities in the water. documentation on what constitutes an entity object is in the Entities folder.
  update(roboPos) the update method is input a 3 piece array [x, y, z] containing the location of the robot and sends out and svr frame for forward and down simulating what the camera's would see. 
"""
