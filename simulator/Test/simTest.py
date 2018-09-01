import seawolf as sw
import numpy as np


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
      print("---------------DONE PRINTING ALL RESULTS-------------")
      for t in tests:
        print t
      
            
