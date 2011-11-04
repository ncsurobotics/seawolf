
from __future__ import division
from math import radians, degrees, sin, cos, pi, atan2
import numpy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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
        glPushMatrix()
        glRotate(self.yaw_offset, 0, 0, -1)
        self.model.draw()
        glPopMatrix()

        # Lines to show fov
        half_fov = radians(self.get_camera_fov("forawrd")/2)
        height = 0
        glColor(0, 1, 0)
        glTranslate(1.5, 0, 0)
        glBegin(GL_LINES)

        glVertex(0, 0, height)
        glVertex(4, 0, height)

        glVertex(0, 0, height)
        glVertex(
            cos(half_fov)*5,
            sin(half_fov)*5,
            height)

        glVertex(0, 0, height)
        glVertex(
            cos(-half_fov)*5,
            sin(-half_fov)*5,
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

        # Convert to homogeneous coordinates (column matrix)
        if len(point) == 3:
            point = numpy.matrix([point[0], point[1], point[2], 1]).transpose()
        elif len(point) == 2:
            point = numpy.matrix([point[0], point[1], 0, 1]).transpose()
        else:
            raise ValueError("point must be length 2 or 3.")

        camera_transform = self.get_camera_matrix(camera)
        new_point = numpy.dot(camera_transform, point)

        # Convert from a column matrix to array
        new_point = numpy.array(new_point.transpose())[0]

        # OpenGL camera is at the origin pointing down the -Z axis.  Using
        # arctargent we can get the spherical angles of the point.
        theta = degrees(atan2(new_point[0], -new_point[2]))
        phi = degrees(atan2(new_point[0], -new_point[1]))

        # Scale from -fov to fov
        half_horizontal_fov = self.get_camera_fov(camera, vertical=False)/2
        half_vertical_fov = self.get_camera_fov(camera, vertical=True)/2
        theta = theta/half_horizontal_fov
        phi = phi/half_vertical_fov

        # Make None if outside fov
        if abs(theta) > self.get_camera_fov(camera)/2:
            theta = None
        if abs(phi) > self.get_camera_fov(camera, vertical=True)/2:
            phi = None

        if len(point) == 2:
            return theta, phi

    def get_camera_fov(self, camera, vertical=False):
        #TODO: What are the real FOVs for the cameras we use?
        if vertical:
            return 53
        else:
            return 53

    def get_camera_matrix(self, camera):
        '''Gets the modelview matrix for the given camera.'''
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.camera_transform(camera)
        # Transpose to format into row major order
        modelview = glGetDouble(GL_MODELVIEW_MATRIX).transpose()
        glPopMatrix()

        return modelview

    def camera_transform(self, camera):

        if camera == "forward":
            ref_point = self.absolute_point((1, 0, 0))
            up = self.absolute_point((0, 0, 1)) - self.pos
            gluLookAt(
                self.pos[0], self.pos[1], self.pos[2],
                ref_point[0], ref_point[1], ref_point[2],
                up[0], up[1], up[2])

        elif camera == "down":
            raise NotImplementedError()

        else:
            raise ValueError('Unknown camera: "%s"' % camera)
