
import seawolf as sw

__all__ = ["yaw", "pitch", "depth", "roll"]


class PIDInterface(object):

    def __init__(self, namespace, setter=None):
        self.namespace = namespace
        self.setter = setter

    @property
    def heading(self):
        return sw.var.get(self.namespace + ".Heading")

    @heading.setter
    def heading(self, value):
        if self.setter is None:
            sw.var.set(self.namespace + ".Heading", value)
        else:
            self.setter(value)

    def pause(self):
        sw.var.set(self.namespace + ".Paused", 1.0)


def set_yaw(value):
    min = -180
    max = 180

    if min <= value <= max:
        sw.var.set("YawPID.Heading", value)
    else:
        raise ValueError(
            "Value for yaw heading must be in range {low} to {high}".format(low=min, high=max)
        )


def set_pitch(value):
    min = -25
    max = 25

    if min <= value <= max:
        sw.var.set("PitchPID.Heading", value)
    else:
        raise ValueError(
            "Value for pitch heading must be in range {low} to {high}".format(low=min, high=max)
        )


def set_roll(value):
    min = -10
    max = 10

    if min <= value <= max:
        sw.var.set("RollPID.Heading", value)
    else:
        raise ValueError(
            "Value for roll heading must be in range {low} to {high}".format(low=min, high=max)
        )


def set_depth(value):
    min = -6
    max = 1

    if min <= value <= max:
        sw.var.set("DepthPID.Heading", value)
    else:
        raise ValueError(
            "Value for depth heading must be in range {low} to {high}".format(low=min, high=max)
        )

yaw = PIDInterface("YawPID", set_yaw)
pitch = PIDInterface("PitchPID", set_pitch)
depth = PIDInterface("DepthPID", set_depth)
roll = PIDInterface("RollPID", set_roll)
