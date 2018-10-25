# this module handles the running of seawolf mission

import seawolf as sw
import svr
import numpy as np
import sw3
import cv2
import sys
import conf

import missions as ms


#Oh god for the love of god this isn't right please make srv a global header
sys.path.append("../../srv")
import srv

sys.path.append("../seawolf/mission_control/missions")


def hubConnect():
  """ connecting to hub """
  sw.loadConfig("../conf/seawolf.conf");
  sw.init("missionControl : Main");

def srvConnect():
  """ connecting to svr """
  #svr.connect()
  sys.path.append("../../srv")
  import os
  print "Directory = ", sys.path
  srv.connect()
  """setting up svr streams """
  forward = srv.stream("forward")
  #forward.unpause()

  down = srv.stream("down")
  #down.unpause()
  sys.path.append("../seawolf/mission_control/missions")

  global cameras 
  cameras = {
             "forward" : forward,
             "down"    : down
            }

DBPRINT = True #False


killName = "MissionReset"


def main():
  """ 
  array of missions to run. all missions should be in the mission module/directory
  missions will run int the order that they are in the array
  """
  if len(sys.argv) != 2:
    raise Exception("TO RUN: python2.7 run.py pathTo.conf")
  missions = conf.readFile(sys.argv[1])
  #missions = [ wheelState.WheelState()  ]
  #missions = [ pathBentState.PathBentState() ]
  runMissions(missions)  

def runMissions(missions, dbprint = True): 
  hubConnect()
  srvConnect()
  global DBPRINT 
  DBPRINT = dbprint
  try:
    for mission in missions:
      mission.setup()
      camera = mission.getCamera()
      running = True
      print "Begining to run: " + mission.getName()
      while running:
        dbPrint("+++++++++++++++++++++++++++++++++++++++++++++++")
        try:
          frame = getFrame(camera)
          running = mission.processFrame(frame)
          cv2.waitKey(1)
        except Exception as e:
          dbPrint( "ERROR running " + mission.getName() + " moving to next")
          dbPrint( e )
          running = False
    
      dbPrint("Done with: " + mission.getName())
      
      #send notification over hub that mission is done
      cmd = ("MISSION_DONE", type(mission).__name__)
      sw.notify.send(*cmd) #send notification to seawolf
      
  except Exception as e:
    dbPrint( e)
    dbPrint( "ERROR occurred when checking errors, stopping running")
  
  finally:
    sw3.Forward(0).start()
    cmd = ("MISSION_DONE", "DONE")
    sw.notify.send(*cmd) #send notification to seawolf
    dbPrint( "done with missions")
    

"""
looks for error conditions and decides what to do when that happens
some to look for:
    killswitch
    pneumaticsLeak (if implemented)
"""
def checkError():
  #checking for killswitch
  dbPrint("checkErr")
  killSw = sw.var.get(killName)
  dbPrint("kill switch %.2f"% killSw)
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
  frame = cameras[camera].getNextFrame()
  #turning frame from cv frame, standard from svr to cv2 frame
  #frame = np.asarray(frame[:, :])
  return frame
  
  
def dbPrint(string):
  if DBPRINT:
    print(string)
  




if __name__ == "__main__":
  main()
