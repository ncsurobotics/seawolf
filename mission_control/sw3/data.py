
import seawolf as sw

__all__ = ["data"]

class Imu(object):
    @property
    def yaw(self):
        return sw.var.get("SEA.Yaw")
    
    @property
    def pitch(self):
        return sw.var.get("SEA.Pitch")
    
    @property
    def roll(self):
        return sw.var.get("SEA.Roll")

class Data(object):
    def __init__(self):
        self.imu = Imu()

    @property
    def depth(self):
        return sw.var.get("Depth")

    @property
    def power_status(self):
        return sw.var.get("PowerStatus")

data = Data()
