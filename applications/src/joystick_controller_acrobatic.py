""" Joystick Control script for Seawolf """

from __future__ import division

import sys
sys.path.append("../mission_control")
from math import sin, cos, pi, sqrt
import argparse

import seawolf as sw
import sw3
import sw3.joystick as joystick
import sw3.ratelimit as ratelimit

# Speed for the hat forward and backward
FORWARD_SPEED = 0.4
MAX_DEPTH_RATE = 0.5 #degrees
MAX_STRAFE_RATE = 0.4
MAX_PITCH_RATE = 0.2
PITCH_ENABLED = True
ROLL_ENABLED = False
DEPTH_HOLD = None # gets defined later


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
    # get joystick values
    angle = event.angle_radians
    mag = max(min(event.magnitude, 1.0), -1.0) #normalization ensures values are complementary
    #print(mag,angle)

    # translate joystick cmds to control variables.
    forward_rate = (mag * sin(angle))
    yaw_rate = (mag * cos(angle))

    use_mission = False
    if use_mission:
        sw3.nav.do(sw3.CompoundRoutine((sw3.SetRotate(yaw_rate), sw3.Forward(forward_rate))))
    else:
        sw.notify.send("THRUSTER_REQUEST", "Forward %.2f" % forward_rate)
        sw.notify.send("THRUSTER_REQUEST", "Yaw %.2f" % yaw_rate)

        
def update_Raxis(event):
    global DEPTH_HOLD
    global ROLL_ENABLED
    #global DEPTH_STEP
    global PITCH_ENABLED
    
    if DEPTH_HOLD==False:
        angle = event.angle_radians
        mag = max(min(event.magnitude, 1.0), -1.0)

        #determine control vectors
        strafe_rate = (mag * cos(angle)) * MAX_STRAFE_RATE
        depth_rate = -(mag * sin(angle)) * MAX_DEPTH_RATE
        #print("depth_rate %2.f, strafe %.2f" % (depth_rate,strafe_rate))
    
        #Send commands to Seawolf
        use_mission = False
        if use_mission:
            sw.notify.send("THRUSTER_REQUEST", "Depth %.2f" % depth_rate)
            sw3.nav.do(sw3.Strafe(strafe))
        else:
            sw.notify.send("THRUSTER_REQUEST", "Strafe %.2f" % strafe_rate)
            sw.notify.send("THRUSTER_REQUEST", "Depth %.2f" % depth_rate)

    elif DEPTH_HOLD==True:
        angle = event.angle_radians
        mag = max(min(event.magnitude, 1.0), -1.0)

        #determine control vectors
        strafe_rate = (mag * cos(angle)) * MAX_STRAFE_RATE
        if PITCH_ENABLED: pitch_rate = (mag * sin(angle)) * MAX_PITCH_RATE
    
        #Send commands to Seawolf
        use_mission = False
        if use_mission:
            sw3.nav.do(sw3.Strafe(strafe))
            if PITCH_ENABLED: sw.notify.send("THRUSTER_REQUEST", "Pitch %.2f" % pitch_rate)
        else:
            sw.notify.send("THRUSTER_REQUEST", "Strafe %.2f" % strafe_rate)
            if PITCH_ENABLED: sw.notify.send("THRUSTER_REQUEST", "Pitch %.2f" % pitch_rate)
        



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

def setup_parser():
    parser = argparse.ArgumentParser(description="Application to test drive seawolf with a game controller")

    parser.add_argument('-c', '--controller', action='store', default='logitech-F310',
                        nargs=1, dest='selected_controller',
                        choices=['logitech-F310', 'logitech-F310S'],
                        help='Specify what kind of controller to configure this program for')

    parser.add_argument('--depth_hold', action='store_true', default=False)

    return parser


def main():
    sw.loadConfig("../conf/seawolf.conf")
    sw.init("Joystick Controller")

    # parse arguments
    global DEPTH_HOLD
    parser  = setup_parser()
    args    = parser.parse_args()
    joystick_name   = args.selected_controller
    DEPTH_HOLD      = args.depth_hold
    
    # get heading initial heading values
    yaw_heading = sw3.data.imu.yaw()
    depth_heading = 0
    forward_heading = 0

    # instantiate pnuematics controller
    peripheral = Peripherals()

    # instantiate joystick class
    devices = joystick.get_devices()
    
    if len(devices) == 0:
        sys.stderr.write("No joysticks found\n")
        sys.exit(1)

    js = joystick.Joystick(devices[0], joystick.LOGITECH)

    # attach functions to analog sticks
    Lrate_limiter = ratelimit.RateLimiter(10, update_Laxis)
    Rrate_limiter = ratelimit.RateLimiter(10, update_Raxis)

    # splash screen usage-prints
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
                    #yaw_heading = sw3.util.add_angle(yaw_heading, -2.5)
                    #sw3.pid.yaw.heading = yaw_heading
                    pass
                elif event.x > 0:
                    #yaw_heading = sw3.util.add_angle(yaw_heading, 2.5)
                    #sw3.pid.yaw.heading = yaw_heading
                    pass
                elif event.y < 0:
                    #forward_heading = FORWARD_SPEED
                    #sw3.nav.do(sw3.Forward(forward_heading))
                    pass
                elif event.y > 0:
                    #forward_heading = -FORWARD_SPEED
                    #sw3.nav.do(sw3.Forward(forward_heading))
                    pass
                else:
                    #forward_heading = 0
                    #sw3.nav.do(sw3.Forward(forward_heading))
                    pass

        elif event.value == 1:
            if event.name == "button1":
                print "Zeroing thrusters"
                sw3.nav.do(sw3.ZeroThrusters())
                depth_heading = 0

            elif event.name == "button2":
                peripheral.fire()
                
            elif event.name == "button3":
                variables = "Depth", "DepthPID.Heading", "SEA.Yaw", "YawPID.Heading"
                print_table(variables, ["%.2f" % sw.var.get(v) for v in variables])
                print

                variables = "Port", "Star", "Bow", "Stern", "StrafeT", "StrafeB"
                print_table(variables, ["%.2f" % sw.var.get(v) for v in variables])
                print

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

            elif event.name == "button5":
                peripheral.next()
                peripheral.printActive()

            elif event.name == "button6":
                if DEPTH_HOLD:
                    depth_heading = max(0, depth_heading - 0.50)
                    sw3.pid.depth.heading = depth_heading
                else:
                    print("Depth holding disabled!!! ignoring depth-change command.")

            elif event.name == "button7":
                peripheral.prev()
                peripheral.printActive()         

            elif event.name == "button8":
                if DEPTH_HOLD:
                    depth_heading = min(8, depth_heading + 0.50)
                    sw3.pid.depth.heading = depth_heading
                else:
                    print("Depth holding disabled!!! ignoring depth-change command.")

            elif event.name == "button9":
                print_help()

            elif event.name == "button10":
                print "Quitting"
                sw3.nav.do(sw3.ZeroThrusters())
                break


    sw.close()

if __name__ == '__main__':
    main()
