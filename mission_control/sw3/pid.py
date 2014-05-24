
import seawolf as sw

__all__ = ["yaw", "pitch", "depth", "strafet", "strafeb"]

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

def set_yaw(value):
    if -180.0 <= value <= 180.0:
        sw.var.set("YawPID.Heading", value)
    else:
        raise ValueError("Value for yaw heading out of range!")

def set_pitch(value):
    if -15.0 <= value <= 15.0:
        sw.var.set("PitchPID.Heading", value)
    else:
        raise ValueError("That sort of pitch is total suicide!")

def set_strafet(value):
	
	#TODO: get correct safe values
    if -15.0 <= value <= 15.0:
        sw.var.set("StrafeTPID.Heading", value)
    else:
        raise ValueError("That sort of strafe is total suicide!")

def set_strafeb(value):
	
	#TODO: get correct safe values
    if -15.0 <= value <= 15.0:
        sw.var.set("StrafeBPID.Heading", value)
    else:
        raise ValueError("That sort of strafeb is total suicide!")

def set_depth(value):
    if 0.0 <= value <= 20.0:
        sw.var.set("DepthPID.Heading", value)
    else:
        raise ValueError("Cowardly refusing to dive so far! (%.4f)" % (value,))

yaw = PIDInterface("YawPID", set_yaw)
pitch = PIDInterface("PitchPID", set_pitch)
depth = PIDInterface("DepthPID", set_depth)
strafet = PIDInterface("StrafeTPID",set_strafet)
strafeb = PIDInterface("StrafeBPID",set_strafeb)

