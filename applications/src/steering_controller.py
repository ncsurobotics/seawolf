
from __future__ import division
import sys
sys.path.append("../mission_control")

from math import sin, cos, pi, sqrt

import seawolf as sw
import sw3
import sw3.joystick as joystick
import sw3.ratelimit as ratelimit

yaw_heading = 0
x_activated = False
y_activated = False

def update_axis(event):
    global yaw_heading
    global x_activated
    global y_activated

    # x and y start out at zero, however, 0 is NOT center!  When an x event
    # comes in, but y has not been touched, y should not react (and vice
    # versa).  This prevents an axis form moving unless it has gotten a nonzero
    # value before.
    if event.x != 0:
        x_activated = True
    if event.y != 0:
        y_activated = True

    if not x_activated:
        turn_rate = 0
    else:
        # Steering wheel goes from left 0 to right 32767.
        # Normalize so 0 is center and scale from -1 to 1.
        turn_rate = (event.x - 32767/2) / (32767/2)

    if not y_activated:
        forward_rate = 0
    elif event.y < 15000:  # Forward
        forward_rate = 1 - event.y / 15000
    elif event.y > 20000:  # Backward
        forward_rate = -1 * (event.y - 20000) / (32767-20000)
    else:
        forward_rate = 0

    if abs(turn_rate) > 0.25:
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.SetRotate(turn_rate),
            sw3.Forward(forward_rate)
        ]))

    else:
        yaw_heading = sw3.data.imu.yaw()
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.SetYaw(yaw_heading),
            sw3.Forward(forward_rate)
        ]))

def print_table(headings, *values):
    max_widths = [max(len(heading), 4) + 1 for heading in headings]
    for vs in values:
        widths = [max(len(v), 4) + 1 for v in vs]
        for i in range(0, len(max_widths)):
            max_widths[i] = max(widths[i], max_widths[i])

    format = "%-*s" * len(headings)
    heading_l = reduce(lambda x, y: x + list(y), zip(max_widths, headings), [])

    print format % tuple(heading_l)
    for vs in values:
        vs_l = reduce(lambda x, y: x + list(y), zip(max_widths, vs), [])
        print format % tuple(vs_l)

def print_help():
    print "Look at the button labels for help."
    print

sw.loadConfig("../conf/seawolf.conf")
sw.init("Steering Wheel Controller")

yaw_heading = sw3.data.imu.yaw()

devices = joystick.get_devices()
if len(devices) == 0:
    sys.stderr.write("No joysticks found\n")
    sys.exit(1)

depth_heading = 0
rate_limiter = ratelimit.RateLimiter(10, update_axis)
js = joystick.Joystick(devices[0], joystick.STEERINGWHEEL)

print_help()

while True:
    event = js.poll()

    if isinstance(event, joystick.Axis):
        if event.name == "wheelAndThrottle":
            rate_limiter.provide(event)

        elif event.name == "padX":
            if event.y < 0:
                yaw_heading = sw3.util.add_angle(yaw_heading, -5)
            elif event.y > 0:
                yaw_heading = sw3.util.add_angle(yaw_heading, 5)
            sw3.pid.yaw.heading = yaw_heading

        elif event.name == "padY" and event.x != 0:
            if event.x > 0:
                depth_heading = min(8, depth_heading + 0.50)
                sw3.pid.depth.heading = depth_heading
            else:
                depth_heading = max(0, depth_heading - 0.50)
                sw3.pid.depth.heading = depth_heading

    elif event.value == 1:

        if event.name == "button1":
            print "Zeroing thrusters"
            sw3.nav.do(sw3.ZeroThrusters())

        elif event.name == "button4":
            while js.poll().name != "button4":
                pass
            print "Press again to confirm breech"
            if js.poll().name == "button4":
                print "Breeching!"
                sw3.nav.do(sw3.EmergencyBreech())
            else:
                print "Canceled."

        elif event.name == "button5":
            print_help()

        elif event.name == "button3":
            variables = "Depth", "DepthPID.Heading", "SEA.Yaw", "YawPID.Heading"
            print_table(variables, ["%.2f" % sw.var.get(v) for v in variables])
            print

            variables = "Port", "Star", "Bow", "Stern", "StrafeT", "StrafeB"
            print_table(variables, ["%.2f" % sw.var.get(v) for v in variables])
            print

        elif event.name == "button6":
            print "Quiting"
            sw3.nav.do(sw3.ZeroThrusters())
            break
