
from __future__ import division
from math import radians, degrees, sin, cos, pi, atan2
import numpy

from OpenGL.GL import *

import seawolf

from base import ModelEntity

class RobotEntity(ModelEntity):

    DEPTH_CONSTANT = 1.5
    VELOCITY_CONSTANT = 1
    YAW_CONSTANT = 40

    def __init__(self, *args, **kwargs):
        super(RobotEntity, self).__init__(*args, **kwargs)

        self.depth = -1*self.pos[2]
        self.tracked_vars = {}
        self.forward_fov = 53

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
        self.yaw = (self.yaw+180) % 360 - 180  # Range -180 to 180
        seawolf.var.set("SEA.Yaw", self.yaw)
        seawolf.notify.send("UPDATED", "IMU")

    def draw(self):
        self.pre_draw()
        self.model.draw()

        # Lines to show fov
        half_fov = radians(self.forward_fov/2)
        height = 1
        glColor(0, 1, 0)
        glBegin(GL_LINES)

        glVertex(0, 0, height)
        glVertex( 0, -4, height)

        glVertex(0, 0, height)
        glVertex(
            sin(half_fov)*5,
            -cos(half_fov)*5,
            height)

        glVertex(0, 0, height)
        glVertex(
            sin(-half_fov)*5,
            -cos(-half_fov)*5,
            height)

        glEnd()

        self.post_draw()

    def find_entity(self, entity_cls):

        entity_found = False
        for entity in self.simulator.entities:
            if entity.__class__.__name__ == entity_cls.__name__:

                entity_found = True
                data = entity.find(self)
                if data:
                    return data

        if not entity_found:
            print "Warning: Entity %s is being searched for, but none exists in the simulator." % entity_cls

        return None

    def find_point(self, camera, point):
        '''Finds a point viewed from the given camera.

        All angles that are returned are expressed as a number from -1 to 1.  0
        is straight ahead, -1 is maximum fov to the left or down, 1 is maximum
        fov to the right or up.

        '''
        assert len(point) == 3 or len(point) == 2
        point = numpy.array(point)

        if camera == "forward":
            if len(point) == 2:
                return self._find_point_forward_2d(point)
            else:
                return self._find_point_forward_3d(point)

        elif camera == "down":
            assert len(point) == 3
            return self._find_point_down(point)

        else:
            raise ValueError('Unknown camera: "%s"' % camera)

    def _find_point_forward_2d(self, point):
        # TODO: Take into account roll
        delta = point - self.pos[0:2]
        angle_to_point = degrees(atan2(-delta[1], delta[0]))
        #angle_to_point = 90 - angle_to_point  # Convert to clockwise positive, straight ahead=0
        relative_angle = angle_to_point - self.yaw
        relative_angle = (relative_angle+180) % 360 - 180  # Range -180 to 180
        if abs(relative_angle) < self.forward_fov/2:
            return relative_angle / (self.forward_fov/2)
        else:
            return None

    def _find_point_forward_3d(self, point):
        raise NotImplementedError()

    def _find_point_down(self, point):
        raise NotImplementedError()

