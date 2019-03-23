# this module handles the running of seawolf mission

import seawolf as sw
import svr
import numpy as np
import sw3
import cv2
import sys
import conf
import time
from subprocess import call, Popen
from multiprocessing import Process
import signal
import datetime
import os

import missions as ms
sys.path.append("../seawolf/mission_control/missions")


def hubConnect():
  """ connecting to hub """
  sw.loadConfig("../conf/seawolf.conf");
  sw.init("missionControl : Main");

def svrConnect():
  """ connecting to svr """
  svr.connect()
  """setting up svr streams """
  forward = svr.Stream("forward")
  forward.unpause()
  down = svr.Stream("down")
  down.unpause()
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
  runMissions(missions)  

def runMissions(missions, dbprint = True, missionFps = 1, autoRecord=True): 
  hubConnect()
  svrConnect()
  global DBPRINT 
  DBPRINT = dbprint
  try:
    if autoRecord:
      mission_start = datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
      os.mkdir('recordings/' + mission_start)
    for mission in missions:
      mission.setup()
      camera = mission.getCamera()
      if autoRecord:
        recordFile = '../mission_control/recordings/' + mission_start + '/' + mission.getName()
        recordProc = Popen(["python", "reccordSVR.py", recordFile, camera], cwd="../vision")
      running = True
      print "Begining to run: " + mission.getName()
      while running:
        dbPrint("+++++++++++++++++++++++++++++++++++++++++++++++")
        try:
          start = time.clock()
          frame = getFrame(camera)
          running = mission.processFrame(frame)
          # wait a frame rate minus the time taken for mission/vision
          time.sleep(max(1.0/missionFps - (time.clock() - start), 0))
          cv2.waitKey(1)
        except Exception as e:
          dbPrint( "ERROR running " + mission.getName() + " moving to next")
          dbPrint( e )
          running = False
    
      dbPrint("Done with: " + mission.getName())
      
      #send notification over hub that mission is done
      cmd = ("MISSION_DONE", type(mission).__name__)
      sw.notify.send(*cmd) #send notification to seawolf

      # stop recording this mission
      if autoRecord:
        os.kill(recordProc.pid, signal.SIGABRT)

      
  except Exception as e:
    dbPrint( e)
    dbPrint( "ERROR occurred when checking errors, stopping running")
  
  finally:
    sw3.Forward(0).start()
    cmd = ("MISSION_DONE", "DONE")
    sw.notify.send(*cmd) #send notification to seawolf
    dbPrint( "done with missions")
    # stop recording this mission
    if autoRecord:
      os.kill(recordProc.pid, signal.SIGABRT)
    

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
  frame = cameras[camera].get_frame()
  #turning frame from cv frame, standard from svr to cv2 frame
  frame = np.asarray(frame[:, :])
  return frame
  
  
def dbPrint(string):
  if DBPRINT:
    print(string)
  




if __name__ == "__main__":
  main()
