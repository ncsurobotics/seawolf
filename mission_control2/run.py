# this module handles the running of seawolf mission

import seawolf as sw
import svr
import numpy as np
import sw3
import cv2
import sys
import conf

import missions as ms

""" connecting to hub """
sw.loadConfig("../conf/seawolf.conf");
sw.init("missionControl : Main");
  
""" connecting to svr """
svr.connect()
"""setting up svr streams """
forward = svr.Stream("forward")
forward.unpause()

down = svr.Stream("down")
down.unpause()

cameras = {
           "forward" : forward,
           "down"    : down
          }




killName = "MissionReset"








def main():

  
  
  """ 
  array of missions to run. all missions should be in the mission module/directory
  missions will run int the order that they are in the array
  """
  if len(sys.argv) != 2:
    raise Exception("TO RUN: python2.7 run.py pathTo.conf")
  missions = conf.readFile(sys.argv[1])
  
  
  try:
    for mission in missions:
      mission.setup()
      camera = mission.getCamera()
      running = True
      print "Begining to run: " + mission.getName()
      while checkError() and running:
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        try:
          frame = getFrame(camera)
          running = mission.processFrame(frame)
          cv2.waitKey(1)
          
        except Exception as e:
          print "hello"
          print "ERROR running " + mission.getName() + " moving to next"
          print e
          running = False
    
      print "Done with: " + mission.getName()  
  except Exception as e:
    print e
    print "ERROR occurred when checking errors, stopping running"
  
  finally:
    sw3.Forward(0).start()
    print "done with missions"
    

"""
looks for error conditions and decides what to do when that happens
some to look for:
    killswitch
    pneumaticsLeak (if implemented)
"""
def checkError():
  #checking for killswitch
  print("checkErr")
  killSw = sw.var.get(killName)
  print("kill switch %.2f"% killSw)
  if abs(killSw - 1.0)  < .05:
    #if the kissSw value is equal to 1 then the robot has been killed
    raise BaseException(killName)
  return True




"""
gets the next frame from svr for the desired camera
camera = string the holds the name for the camera in svr
returns numpy array of frame from svr
"""
def getFrame(camera):
  frame = cameras[camera].get_frame()
  #turning frame from cv frame, standard from svr to cv2 frame
  frame = np.asarray(frame[:, :])
  return frame
  
  
  
  




if __name__ == "__main__":
  main()
