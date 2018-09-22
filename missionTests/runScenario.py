import sys
import Conf
from multiprocessing import Process

#importing the simulator
sys.path.append('../simulator')
from sim import main as simMain
from Test.simTest import runTest 

#importing the missions
sys.path.append('../mission_control')
from run import *

import time

def main():
  if len(sys.argv) != 2:
    print("ERROR: expected 1 command line arguement")
    print("ERROR: run as python run.py <confFile>")
    quit()
  ents, tests, miss = Conf.readFile(sys.argv[1])
  
  #making the simulator process
  simProcess = Process(target = simMain, args = (ents, ))
  simProcess.start()
  
  #making the test process
  testProcess = Process(target = runTest, args = (tests, ))
  testProcess.start()
  
  #this sleep is to make sure the simulator has connected to svr before mission tries to
  time.sleep(3)
  
  #making the mission running process
  missionProcess = Process(target = runMissions, args = (miss, ))
  missionProcess.start()
  
  #wait until the mission is done
  missionProcess.join()
  
  #wait for test process to be done
  testProcess.join()
 
  raw_input("press enter to stop sim")
  #killing the simulator
  simProcess.terminate()
  
  
  
  
 
  
  
  





if __name__ == "__main__":
  main()
