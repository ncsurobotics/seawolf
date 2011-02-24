
import copy
import glob
import math
import select
import struct

class JoystickDriver(object):
    EVENT_BUTTON = 0x01
    EVENT_AXIS = 0x02
    EVENT_INIT = 0x80

    def __init__(self, device_path):
        self.path = device_path
        self.dev = open(self.path, "r")
        self.struct = struct.Struct("@IhBB")

    def _unpack(self, s):
        unpacked = self.struct.unpack(s)
        return dict(zip(("time", "value", "type", "number"), unpacked))

    def get_event(self):
        s = self.dev.read(self.struct.size)
        return self._unpack(s)
    
    def close(self):
        self.dev.close()

class Axis(object):
    def __init__(self, axis, name=None):
        self.axis = axis
        self.name = name
        self.x = 0
        self.y = 0

    @property
    def mag(self):
        scalar = 1.0 / 32767
        return (self.x**2 + self.y**2)**0.5 * scalar

    @property
    def angle(self):
        x, y = self.x, -self.y

        if x == 0 and y < 0:
            return -180
        elif x == 0:
            return 0

        base = math.atan(float(abs(y)) / abs(x))
        angle = base * 360 / (2 * math.pi)
        angle = 90 - angle

        if x >= 0 and y >= 0:
            return angle
        elif x <= 0 and y >= 0:
            return -angle
        elif x <= 0 and y <= 0:
            return -180 + angle
        else:
            return 180 - angle

    def __repr__(self):
        return "%s: (%d, %d)" % (self.name, self.x, self.y)

class Button(object):
    def __init__(self, number, name=None):
        self.number = number
        self.name = name
        self.value = 0

    def __repr__(self):
        return "%s: %d" % (self.name, self.value)

class Joystick(object):
    def __init__(self, device_path, mapping):
        self.joystick = JoystickDriver(device_path)
        self.mapping = mapping
        self.axises = dict()
        self.buttons = dict()

        for i in self.mapping:
            if isinstance(i, Button):
                self.buttons[i.number] = i
            elif isinstance(i, Axis):
                self.axises[i.axis[0]] = i
                self.axises[i.axis[1]] = i

    def poll(self):
        event = None
        event_type = JoystickDriver.EVENT_INIT

        while event_type & JoystickDriver.EVENT_INIT:
            event = self.joystick.get_event()
            event_type = event["type"]

        event_number = event["number"]
        event_value = event["value"]
        
        if event_type & JoystickDriver.EVENT_BUTTON:
            button = self.buttons[event_number]
            button.value = event_value
            return copy.deepcopy(button)

        elif event_type & JoystickDriver.EVENT_AXIS:
            axis = self.axises[event_number]

            if event_number == axis.axis[0]:
                axis.x = event_value
            else:
                axis.y = event_value

            return copy.deepcopy(axis)

        else:
            raise Exception("Unsupported event")

    def close(self):
        self.joystick.close()

def get_devices():
    return glob.glob("/dev/js*") + glob.glob("/dev/input/js*")

LOGITECH = (Axis((0, 1), "leftStick"),
            Axis((2, 3), "rightStick"),
            Axis((4, 5), "hat"),
            Button(0, "button1"),
            Button(1, "button2"),
            Button(2, "button3"),
            Button(3, "button4"),
            Button(4, "button5"),
            Button(5, "button6"),
            Button(6, "button7"),
            Button(7, "button8"),
            Button(8, "button9"),
            Button(9, "button10"),
            Button(10, "leftStickButton"),
            Button(11, "rightStickButton"))
