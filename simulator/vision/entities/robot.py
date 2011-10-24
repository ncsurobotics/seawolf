
from math import radians, sin, cos

import seawolf

from base import ModelEntity

class RobotEntity(ModelEntity):

    DEPTH_CONSTANT = 1.5
    VELOCITY_CONSTANT = 0.7
    YAW_CONSTANT = 40

    def __init__(self, *args, **kwargs):
        super(RobotEntity, self).__init__(*args, **kwargs)

        self.depth = -1*self.pos[2]
        self.tracked_vars = {}

        seawolf.var.subscribe("Port")
        seawolf.var.subscribe("Star")
        seawolf.var.subscribe("Bow")
        seawolf.var.subscribe("Stern")

    def get_var(self, name):
        if seawolf.var.stale(name) or name not in self.tracked_vars:
            value = seawolf.var.get(name)
            self.tracked_vars[name] = value
            return value
        else:
            return self.tracked_vars[name]

    def step(self, dt):

        # Thrusters
        port = self.get_var("Port")
        star = self.get_var("Star")
        bow = self.get_var("Bow")
        stern = self.get_var("Stern")

        # Depth
        self.depth = self.depth + (bow+stern) * self.DEPTH_CONSTANT * dt
        if self.depth < 0:
            self.depth = self.depth + 1.0*dt
        self.pos[2] = -1*self.depth
        seawolf.var.set("Depth", self.depth)

        # Velocity
        velocity = (port + star) * self.VELOCITY_CONSTANT

        # Position
        self.pos[0] += cos(radians(-self.yaw)) * velocity * dt
        self.pos[1] += sin(radians(-self.yaw)) * velocity * dt

        # Yaw
        self.yaw = self.yaw + (port-star) * self.YAW_CONSTANT * dt
        self.yaw = (self.yaw+180) % 360 - 180
        seawolf.var.set("SEA.Yaw", self.yaw)
        seawolf.notify.send("UPDATED", "IMU")

    def find_entity(self, entity_cls):

        entity_found = False
        for entity in self.simulator.entities:
            if entity.__class__.__name__ == entity_cls.__name__:

                entity_found = True
                print "FOUND MATCHING CLASS:", entity, entity_cls
                data = entity.find(self)
                if data:
                    return data

        if not entity_found:
            print "Warning: Entity %s is being searched for, but none exists in the simulator." % entity_cls

        return None

