from multiprocessing import Process
import seawolf as sw
import numpy as np

class SimTest(object):
  
  def __init__(self, tests):
    self.pos = np.float32([0, 0, 0])
    t = Process(target=runTest, args= (tests, ))
    t.start()
    
  
  def updatePosition(self, position):
    #updating the position in hub so that test cases can use it, utitlities.py must be modified if these names change
    sw.var.set('Sim.xLoc', position[0])
    sw.var.set('Sim.yLoc', position[1])
    sw.var.set('Sim.zLoc', position[2])



def runTest(tests):
    sw.loadConfig("../conf/seawolf.conf");
    sw.init("Simulator : Test");
    sw.notify.filter(sw.FILTER_ACTION, "MISSION_DONE"); 
    try:  
      while True:
        (event, msg) = sw.notify.get()
        if (event == "MISSION_DONE" and msg == "DONE"):
          break
        if (event == "MISSION_DONE"): 
          for test in [test for test in tests if test.missionName == msg]:
            test.run()
            print test
    finally:
      print "in finally"
      for t in [test for test in tests if not test.wasRan()]:
        print t
      
            
