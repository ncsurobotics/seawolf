Missions handle the logic of seawolf when it attempts to do something. 

mission uses a vision import to get a measurement of where the thing it is looking for is. 

mission uses sw3 to get the robot to go to where it wants. 

a mission must implement the following function:
  
  
  getCamera()
    returns a string with the name of the camera to use. 
    the available cameras are:
        forward
        down
  
  
  getName()
    returns the name of mission, typically this should be similar to the file name
    
  
  setup()
    the setup function runs right before the mission is started. It should do the following:
        set desired starting depth
        set desired starting forward speed
        iniate/reset startTime and other counts/variables for the mission
  
  
  processFrame(frame)
    this function should be the meat of the mission.
    it is passed camera frame, aka a numpy array of size [x, x, 3], to be analyzed by the imported vision module
    the vision module returns an objec that has .found() method and others
    the mission uses the returned object to decide what to do
    typically the mission, and the obj returned by the vision will be heavily linked. 
