
import seawolf as sw

__all__ = ["yaw", "pitch", "rotate", "depth"]

class PIDInterface(object):
    def __init__(self, namespace, setter=None):
        self.namespace = namespace
        self.setter = setter

    @property
    def heading(self):
        return sw.var.get(self.namespace + ".Heading")

    @heading.setter
    def heading(self, value):
        if self.setter == None:
            sw.var.set(self.namespace + ".Heading", value)
        else:
            self.setter(value)

    def pause(self):
        sw.var.set(self.namespace + ".Paused", 1.0)

def set_yaw(self, value):
    if -180.0 <= value <= 180:
        sw.var.set("RotatePID.Paused", 1.0)
        sw.var.set("YawPID.Heading", value)
    else:
        raise ValueError("Value for yaw heading out of range!")

def set_pitch(self, value):
    if -15.0 <= value <= 15.0:
        sw.var.set("PitchPID.Heading", value)
    else:
        raise ValueError("That sort of pitch is total suicide!")

def set_rotate(self, value):
    if -20.0 <= value <= 20:
        sw.var.set("YawPID.Paused", 1.0)
        sw.var.set("RotatePID.Heading", value)
    else:
        raise ValueError("Value for rotate heading complete senseless you silly baffoon!")

def set_depth(self, value):
    if 0 <= depth <= 20:
        sw.var.set("DepthPID.Heading", value)
    else:
        raise ValueError("Cowardly refusing to dive so far!")

yaw = PIDInterface("Yaw", set_yaw)
pitch = PIDInterface("Pitch", set_pitch)
rotate = PIDInterface("Rotate", set_rotate)
depth = PIDInterface("Depth", set_depth)
