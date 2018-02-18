import sys
import time
import seawolf as sw

sys.path.append('../../mission_control/')
import sw3

from calibrate import test

#connecting to hub
sw.loadConfig("../../conf/seawolf.conf")
sw.init("Simulator : CalibrateDepth")


#value at surface
surVal = 0
values = [surVal,
					surVal + 2,
					surVal + 3,
					surVal,
					surVal + 3,
					surVal,
					surVal + 4,
					surVal + 2,
					surVal + 4,
					surVal
				]
test(sw3.SetDepth, values, .2)
