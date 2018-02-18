import sys
import time
import seawolf as sw

sys.path.append('../../mission_control/')
import sw3

from calibrate import test

#connecting to hub
sw.loadConfig("../../conf/seawolf.conf")
sw.init("Simulator : CalibrateYaw")




		

test(sw3.RelativeYaw, [10, -10, -20, 20, 45, -45], 1)


