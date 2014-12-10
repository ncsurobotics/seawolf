"""
Linux joystick driver created using Linux joystick API
https://www.kernel.org/doc/Documentation/input/joystick-api.txt
"""

from __future__ import division, print_function

import copy
import glob
import math
import struct


def get_devices():
    """ Return a list of connected joystick devices
    """
    return glob.glob("/dev/js*") + glob.glob("/dev/input/js*")


class JoystickDriver(object):

    EVENT_BUTTON = 0x01
    EVENT_AXIS = 0x02
    EVENT_INIT = 0x80
    EVENT_FORMAT = "@IhBB"  # [uint][short][char][char]
    EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

    def __init__(self, device_path):
        self.path = device_path
        self.dev = open(self.path, "rb")
        self.dev.flush()
        self.struct = struct.Struct(JoystickDriver.EVENT_FORMAT)

    def _unpack(self, s):
        unpacked = self.struct.unpack(s)
        return dict(zip(("time", "value", "type", "number"), unpacked))

    def get_event(self):
        s = self.dev.read(JoystickDriver.EVENT_SIZE)
        return self._unpack(s)

    def close(self):
        self.dev.close()


class Button(object):

    def __init__(self, number, name=None):
        self.number = number
        self.name = name
        self.value = 0

    def __repr__(self):
        return "{name}: {val}".format(name=self.name, val=self.value)


class Axis(object):

    def __init__(self, axis, name=None):
        self.axis = axis
        self.name = name
        self.x = 0
        self.y = 0

    @property
    def magnitude(self):
        """ Returns the current magnitude of the stick
        """
        scalar = 1.0 / 32767
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2)) * scalar

    @property
    def angle_degrees(self):
        """ Returns the angle of the stick in degrees, from -180 to 180, with 0 at due east
        """
        return math.degrees(self.angle_radians)

    @property
    def angle_radians(self):
        """ Returns the angle of the stick in radians, from -pi to pi, with 0 at due east
        """
        x, y = self.x, -self.y

        if x == 0:
            if y > 0:
                return math.pi / 2
            else:
                return -math.pi / 2

        return math.atan2(y, x)

    @property
    def bearing_degrees(self):
        """ Returns the angle of the stick in degrees, from -180 to 180, with 0 at due north
        """
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

    @property
    def bearing_radians(self):
        """ Returns the angle of the stick in degrees, from -pi to pi, with 0 at due north
        """
        return math.radians(self.bearing_degrees)

    def __repr__(self):
        return "{name}: ({x}, {y})".format(name=self.name, x=self.x, y=self.y)


class Joystick(object):

    def __init__(self, device_path, mapping):
        self.joystick = JoystickDriver(device_path)
        self.mapping = mapping
        self.axes = dict()
        self.buttons = dict()

        for i in self.mapping:
            if isinstance(i, Button):
                self.buttons[i.number] = i
            elif isinstance(i, Axis):
                self.axes[i.axis[0]] = i
                self.axes[i.axis[1]] = i

    def poll(self):
        # Here be magic
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
            axis = self.axes[event_number]

            if event_number == axis.axis[0]:
                axis.x = event_value
            else:
                axis.y = event_value

            return copy.deepcopy(axis)

        else:
            raise Exception("Unsupported event")

    def close(self):
        self.joystick.close()


LOGITECH = (
    Axis((0, 1), "leftStick"),
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
    Button(11, "rightStickButton")
)

STEERINGWHEEL = (
    Axis((0, 1), "wheelAndThrottle"),
    Axis((2, 3), "padX"),
    Axis((4, 5), "padY"),
    Button(0, "button1"),
    Button(1, "button2"),
    Button(2, "button3"),
    Button(3, "button4"),
    Button(4, "button5"),
    Button(5, "button6"),
    Button(6, "button7"),
    Button(7, "button8"),
    Button(8, "button9"),
    Button(9, "button10")
)

# Testing purposes only
if __name__ == '__main__':
    available = get_devices()

    if len(available) < 1:
        print("No joystick available")

    testj = Joystick(available[0], LOGITECH)

    while True:
        print(testj.poll())
