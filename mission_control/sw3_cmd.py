
import seawolf as sw
from sw3 import *

sw.loadConfig("../conf/seawolf.conf")
sw.init("SW3 Command Line Interface")


def zero_thrusters():
    # nav.clear()
    nav.do(NullRoutine())

    pid.yaw.pause()
    pid.rotate.pause()
    pid.pitch.pause()
    pid.depth.pause()

    mixer.depth = 0
    mixer.pitch = 0
    mixer.yaw = 0
    mixer.forward = 0
    mixer.strafe = 0

EB = emergency_breech
ZT = zero_thrusters
zt = ZT
