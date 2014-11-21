
import sys
sys.path.append("../mission_control")

from math import sin, cos, pi, sqrt

import seawolf as sw
import sw3
import sw3.joystick as joystick
import sw3.ratelimit as ratelimit

# Speed for the hat forward and backward
FORWARD_SPEED = 0.4

yaw_heading = 0


def update_axis(event):
    global yaw_heading
    angle = event.math_angle

    mag = max(min(event.mag, 1.0), -1.0)

    forward = (mag * sin(angle))
    rate = (mag * cos(angle))

    total = abs(forward) + abs(rate)

    if total == 0:
        yaw_heading = sw3.data.imu.yaw()
        sw3.nav.do(sw3.CompoundRoutine((sw3.SetYaw(yaw_heading), sw3.Forward(forward))))
    else:
        for_p = forward / total
        rate_p = rate / total

        total = min(total, 1.0)
        forward = for_p * total
        rate = rate_p * total

        sw3.nav.do(sw3.CompoundRoutine((sw3.SetRotate(rate), sw3.Forward(forward))))


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
    print "R1: Depth up   R2: Depth down"
    print "Button1: Zero thrusters   Button3: Print variables"
    print "Button4: Emergency breech (requires confirmation)"
    print "Left Joystick: Navigate"
    print "Button9: Help   Button10: Quit"
    print

sw.loadConfig("../conf/seawolf.conf")
sw.init("Joystick Controller")

yaw_heading = sw3.data.imu.yaw()

devices = joystick.get_devices()
if len(devices) == 0:
    sys.stderr.write("No joysticks found\n")
    sys.exit(1)

depth_heading = 0
forward_heading = 0
rate_limiter = ratelimit.RateLimiter(10, update_axis)
js = joystick.Joystick(devices[0], joystick.LOGITECH)

print_help()

while True:
    event = js.poll()

    if isinstance(event, joystick.Axis):
        if event.name == "leftStick":
            rate_limiter.provide(event)
        elif event.name == "hat":
            if event.x < 0:
                yaw_heading = sw3.util.add_angle(yaw_heading, -2.5)
                sw3.pid.yaw.heading = yaw_heading
            elif event.x > 0:
                yaw_heading = sw3.util.add_angle(yaw_heading, 2.5)
                sw3.pid.yaw.heading = yaw_heading
            elif event.y < 0:
                forward_heading = FORWARD_SPEED
                sw3.nav.do(sw3.Forward(forward_heading))
            elif event.y > 0:
                forward_heading = -FORWARD_SPEED
                sw3.nav.do(sw3.Forward(forward_heading))
            else:
                forward_heading = 0
                sw3.nav.do(sw3.Forward(forward_heading))

    elif event.value == 1:
        if event.name == "button8":
            depth_heading = min(8, depth_heading + 0.50)
            sw3.pid.depth.heading = depth_heading

        elif event.name == "button6":
            depth_heading = max(0, depth_heading - 0.50)
            sw3.pid.depth.heading = depth_heading

        elif event.name == "button1":
            print "Zeroing thrusters"
            sw3.nav.do(sw3.ZeroThrusters())
            depth_heading = 0

        elif event.name == "button4":
            while js.poll().name != "button4":
                pass
            print "Press again to confirm breech"
            if js.poll().name == "button4":
                print "Breeching!"
                sw3.nav.do(sw3.EmergencyBreech())
                depth_heading = 0
            else:
                print "Canceled."

        elif event.name == "button9":
            print_help()

        elif event.name == "button3":
            variables = "Depth", "DepthPID.Heading", "SEA.Yaw", "YawPID.Heading"
            print_table(variables, ["%.2f" % sw.var.get(v) for v in variables])
            print

            variables = "Port", "Star", "Bow", "Stern", "StrafeT", "StrafeB"
            print_table(variables, ["%.2f" % sw.var.get(v) for v in variables])
            print

        elif event.name == "button10":
            print "Quiting"
            sw3.nav.do(sw3.ZeroThrusters())
            break
