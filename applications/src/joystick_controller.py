
import sys
sys.path.append("../mission_control")

import seawolf as sw
import sw3
import sw3.joystick as joystick
import sw3.ratelimit as ratelimit

sw.loadConfig("../conf/seawolf.conf")
sw.init("Joystick Controller")

devices = joystick.get_devices()
if len(devices) == 0:
    sys.stderr.write("No joysticks found\n")
    sys.exit(1)

depth_heading = 0
yaw_heading = sw3.data.imu.yaw

def update_axis(event):
    angle = event.angle

    forward = max(-1.0, min((-event.y) / 32767.0, 1.0))
    rate = angle / 9

    if abs(rate) < 5:
        sw3.nav.do(sw3.CompoundRoutine((sw3.HoldYaw(), sw3.Forward(foward))))
    else:
        sw3.nav.do(sw3.CompoundRoutine((sw3.SetRotate(rate), sw3.Forward(forward))))
    print "%.2f %4d" % (mag, int(angle))

def zero_thrusters():
    print "Zeroing thrusters"
    sw3.pid.yaw.pause()
    sw3.pid.rotate.pause()
    sw3.pid.pitch.pause()
    sw3.pid.depth.pause()
    
    sw3.mixer.depth = 0
    sw3.mixer.pitch = 0
    sw3.mixer.yaw = 0
    sw3.mixer.forward = 0
    sw3.mixer.strafe = 0
    
    for v in ("Port", "Star", "Bow", "Stern", "Strafe"):
        sw.var.set(v, 0)

rate_limiter = ratelimit.RateLimiter(10, update_axis)
js = joystick.Joystick(devices[0], joystick.logitech)

breech_count = 1

while True:
    event = js.poll()
    if isinstance(event, joystick.Axis):
        if event.name == "leftStick":
            rate_limiter.provide(event)

    elif event.value == 1:
        if event.name == "button8":
            depth_heading = min(8, depth_heading + 0.50)
            sw3.pid.depth.heading = depth_heading

        elif event.name == "button6":
            depth_heading = max(0, depth_heading - 0.50)
            sw3.pid.depth.heading = depth_heading

        elif event.name == "button9":
            zero_thrusters()

        elif event.name == "button4":
            if breech_count == 0:
                print "Breeching!"
                # breech()
            else:
                breech_count -= 1
                print "Press again to confirm emergency breech"
                continue

        breech_count = 1
            
    elif event.name == "button10" and event.value == 0:
        print "Quiting"
        zero_thrusters()
        break
