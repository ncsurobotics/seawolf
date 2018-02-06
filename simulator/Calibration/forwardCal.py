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




try:
	a = sw3.Forward(.9, timeout = -1)

	a.start()
	startTime = time.time()
	i = 0
	while True:
		if i == 0:
			i += 1
			print("enter ctrl-c to stop and get time")
		

finally:
	print ("Total time %5.3f" % (time.time() - startTime))
	sw3.Forward(0).start()
  

