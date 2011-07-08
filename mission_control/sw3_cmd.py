
import seawolf as sw
from sw3 import *

sw.loadConfig("../conf/seawolf.conf")
sw.init("SW3 Command Line Interface")

def zero_thrusters():
    #nav.clear()
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

def square():
    nav.clear()
    a = data.imu.yaw
    nav.append(Forward(0.6, timeout=5))
    nav.append(SetYaw(util.add_angle(a, 90)))
    nav.append(Forward(0.6, timeout=5))
    nav.append(SetYaw(util.add_angle(a, 180)))
    nav.append(Forward(0.6, timeout=5))
    nav.append(SetYaw(util.add_angle(a, 270)))
    nav.append(Forward(0.6, timeout=5))
    return nav.append(SetYaw(a))

EB = emergency_breech
ZT = zero_thrusters
zt = ZT

