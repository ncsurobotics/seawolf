import sys
import seawolf as sw
import time
sys.path.append('../../mission_control/')
import sw3



#connecting to hub
sw.loadConfig("../../conf/seawolf.conf")
sw.init("Simulator : CalibrateForward")


"""
makes robot go forward for a while
"""




def main():
  speeds = [.2, .4, .6, .8, .95]
  for speed in speeds:
    print("Running speed: %.3f" % (speed))
    a = sw3.Forward(speed, timeout = -1)
    raw_input("Press enter to start")
    a.start()
    startTime = time.time()
    raw_input("Press enter to stop")
    sw3.Forward(speed, timeout = -1).start()
    print ("Total time %5.3f" % (time.time() - startTime))

if __name__ == "__main__":
  main()
	
  

