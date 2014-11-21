
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


limits = {
    "yaw.max": 180.0,
    "yaw.min": -180.0,
    "roll.max": 180.0,
    "roll.min": -180.0,
    "pitch.max": 180.0,
    "pitch.min": -180.0,
    "depth.max": 20.0,
    "depth.min": 0.0,
}


def set_yaw(value):
    if limits['yaw.min'] <= value <= limits['yaw.max']:
        sw.var.set("YawPID.Heading", value)
    else:
        raise ValueError("Value for yaw heading must be in range {low} to {high}".format(
            low=limits['yaw.min'], high=limits['yaw.max'])
        )


def set_pitch(value):
    if limits['pitch.min'] <= value <= limits['pitch.max']:
        sw.var.set("PitchPID.Heading", value)
    else:
        raise ValueError("Value for pitch heading must be in range {low} to {high}".format(
            low=limits['pitch.min'], high=limits['pitch.max'])
        )


def set_roll(value):
    if limits['roll.min'] <= value <= limits['roll.max']:
        sw.var.set("RollPID.Heading", value)
    else:
        raise ValueError("Value for roll heading must be in range {low} to {high}".format(
            low=limits['roll.min'], high=limits['roll.max'])
        )


def set_depth(value):
    if limits['depth.min'] <= value <= limits['depth.max']:
        sw.var.set("DepthPID.Heading", value)
    else:
        raise ValueError("Cowardly refusing to dive so far! (%.4f)" % (value,))

yaw = PIDInterface("YawPID", set_yaw)
pitch = PIDInterface("PitchPID", set_pitch)
depth = PIDInterface("DepthPID", set_depth)
roll = PIDInterface("RollPID", set_roll)
