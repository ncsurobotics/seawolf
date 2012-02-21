
import seawolf as sw

__all__ = ["data"]

VARS_TO_FREEZE = ["SEA.Yaw", "Depth"]

class Imu(object):
    def __init__(self, data):
        self.data = data

    def yaw(self, freeze_name=None):
        return self.data.var_get("SEA.Yaw", freeze_name=None)

    def pitch(self):
        return self.data.var_get("SEA.Pitch")

    def roll(self):
        return self.data.var_get("SEA.Roll")

class Data(object):
    def __init__(self):
        self.imu = Imu(self)
        self.freezes = {}  # Map freeze name to variable dictionary

    def depth(self, freeze_name=None):
        return self.var_get("Depth", freeze_name=None)

    def power_status(self):
        return self.var_get("PowerStatus")

    def var_get(self, var, freeze_name=None):
        if freeze_name in self.freezes and var in self.freezes[freeze_name]:
            return self.freezes[freeze_name][var]
        else:
            return sw.var.get(var)

    def freeze(self, freeze_name=None):
        variables = {}
        for var in VARS_TO_FREEZE:
            variables[var] = sw.var.get(var)
        self.freezes[freeze_name] = variables

        # Set Default Freeze
        self.freezes[None] = variables

data = Data()
