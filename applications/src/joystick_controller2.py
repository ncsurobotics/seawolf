""" Joystick Control script for Seawolf """

from __future__ import division

import sys
sys.path.append("../mission_control")

from math import sin, cos, pi, sqrt

import seawolf as sw
import sw3
import sw3.joystick as joystick
import sw3.ratelimit as ratelimit

# Speed for the hat forward and backward
FORWARD_SPEED = 0.4
MAX_PITCH = 10 #degrees
MAX_PITCH_RATE = 0.4
MAX_STRAFE = 0.4
MAX_STRAFE_RATE = 0.4
PITCH_ENABLED = True

yaw_heading = 0

CONTROL_DOC = """\
Controls:
    Navigate:         Left Joystick
    Depth Up:         R1
    Depth Down:       R2
    Zero Thrusters:   Button1
    Emergency Breech: Button4 (requires confirmation)

    Print Variables:  Button3
    Help:             Button9
    Quit:             Button10
"""

class Peripherals(object):
    def __init__(self):
        self.arsenal = [
            self._createDevice('Grabber2','PN',1),
            self._createDevice('Grabber1','PN',2),
            self._createDevice('Torpedo2','PN',3),
            self._createDevice('Torpedo1','PN',4),
            self._createDevice('Dropper2','PN',5),
            self._createDevice('Dropper1','PN',6),
        ]

        self.sel = 0

    def _createDevice(self, name, subsystem, ID):
        device = {'name':name, 'subsystem':subsystem, 'id':ID}
        return device

    def next(self):
        self.sel = (self.sel +1) % len(self.arsenal)

    def prev(self):
        self.sel = (self.sel -1) % len(self.arsenal)

    def printActive(self):
        name =  self.arsenal[self.sel]['name']
        print("currently active device: %s" % name)

    def fire(self):
        name =  self.arsenal[self.sel]['name']
        ID = self.arsenal[self.sel]['id']
        subsystem = self.arsenal[self.sel]['subsystem']

        if (subsystem=='PN'):
            cmd = ("PNEUMATICS_REQUEST", "fire %d" % ID)
            sw.notify.send(*cmd) #send notification to seawolf

            #print what just happend
            print("%s %s" % cmd)
            

    
        

def update_Laxis(event):
    global yaw_heading
    angle = event.angle_radians
    mag = max(min(event.magnitude, 1.0), -1.0)

    forward = (mag * sin(angle))
    rate = (mag * cos(angle))

    total = abs(forward) + abs(rate)

    #Send commands to Seawolf
    sw.notify.send("THRUSTER_REQUEST", "Forward %.4f" % (forward))
    sw.notify.send("THRUSTER_REQUEST", "Yaw %.4f" % (rate))

        
def update_Raxis(event):
    global yaw_heading
    angle = event.angle_radians
    mag = max(min(event.magnitude, 1.0), -1.0)

    #determine control vectors
    pitch_stk = (mag * sin(angle))
    strafe_stk = (mag * cos(angle))
    
    pitch = (-1) * pitch_stk * MAX_PITCH_RATE
    strafe = strafe_stk * MAX_STRAFE_RATE
    
    #Send commands to Seawolf
    sw.notify.send("THRUSTER_REQUEST", "Strafe %.4f" % (strafe))
    sw.notify.send("THRUSTER_REQUEST", "Pitch %.4f" % (pitch))



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
    print CONTROL_DOC


def main():
    sw.loadConfig("../conf/seawolf.conf")
    sw.init("Joystick Controller")

    yaw_heading = sw3.data.imu.yaw()

    devices = joystick.get_devices()
    peripheral = Peripherals()
    if len(devices) == 0:
        sys.stderr.write("No joysticks found\n")
        sys.exit(1)

    depth_heading = 0
    forward_heading = 0
    Lrate_limiter = ratelimit.RateLimiter(10, update_Laxis)
    Rrate_limiter = ratelimit.RateLimiter(10, update_Raxis)
    js = joystick.Joystick(devices[0], joystick.LOGITECH)

    print_help()
    peripheral.printActive()

    while True:
        event = js.poll()

        if isinstance(event, joystick.Axis):
            if (event.name == "leftStick") :
                Lrate_limiter.provide(event)
                
            elif (event.name=="rightStick"):
                Rrate_limiter.provide(event)
                
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
                print "Quitting"
                sw3.nav.do(sw3.ZeroThrusters())
                break

            elif event.name == "button5":
                peripheral.next()
                peripheral.printActive()

            elif event.name == "button7":
                peripheral.prev()
                peripheral.printActive()         

            elif event.name == "button2":
                peripheral.fire()

    sw.close()

if __name__ == '__main__':
    main()
