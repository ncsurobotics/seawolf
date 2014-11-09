
from __future__ import division
from math import radians, sin, cos

import numpy

from OpenGL.GL import *
from OpenGL.GLUT import *


class Container(object):

    '''a blank container object'''

    def __repr__(self):
        return str(self.__dict__)


class Entity(object):

    def __init__(self, pos, color=(0.5, 0.5, 0.5), yaw=0, pitch=0, roll=0):
        assert len(color) == 3 or len(color) == 4
        self.set_pos(pos)
        self.color = color
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.simulator = None

    def _register_simulator(self, simulator):
        self.simulator = simulator

    def set_pos(self, pos):
        assert len(pos) == 3
        self.pos = numpy.array(pos, numpy.float)

    def step(self, dt):
        pass

    def absolute_point(self, point):
        assert len(point) == 2 or len(point) == 3

        if len(point) == 2:

            # Column vector
            point = numpy.array(point).transpose()

            # Generate rotation matrix
            yaw = radians(-self.yaw)
            rotation = numpy.array([
                [cos(yaw), -sin(yaw)],
                [sin(yaw), cos(yaw)],
            ])

            abs_position = numpy.dot(rotation, point) + self.pos[0:2]
            return abs_position

        else:

            # Convert to homogeneous coordinates (column matrix)
            point = numpy.matrix([point[0], point[1], point[2], 1]).transpose()

            # Get modelview matrix for this entity
            # Load the identity first so camera location doesn't affect this
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            self.pre_draw()
            # Transpose to format into row major order
            modelview = glGetDouble(GL_MODELVIEW_MATRIX).transpose()
            self.post_draw()
            glPopMatrix()

            new_point = numpy.dot(modelview, point)
            # Convert from a column matrix to array
            new_point = numpy.array(new_point.transpose())[0]

            return new_point[0:3] / new_point[3]

    def pre_draw(self):
        #glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslate(self.pos[0], self.pos[1], self.pos[2])
        glRotate(self.pitch, 0, 1, 0)
        glRotate(self.roll, 1, 0, 0)
        glRotate(self.yaw, 0, 0, -1)

    def draw(self):
        self.pre_draw()
        self.post_draw()

    def post_draw(self):
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def find(self, robot):
        raise NotImplementedError("This entity is not searchable.  Implement the find method to add this functionality.")


class ModelEntity(Entity):

    def __init__(self, model, yaw_offset=0, *args, **kwargs):
        self.model = model
        self.yaw_offset = yaw_offset
        super(ModelEntity, self).__init__(*args, **kwargs)

    def draw(self):
        self.pre_draw()
        glRotate(self.yaw_offset, 0, 0, -1)
        self.model.draw()
        self.post_draw()


class CubeEntity(Entity):

    def __init__(self, size, *args, **kwargs):
        self.size = size
        super(CubeEntity, self).__init__(*args, **kwargs)

    def draw(self):
        self.pre_draw()
        glutSolidCube(self.size)
        self.post_draw()


class AxisEntity(Entity):

    def __init__(self, pos=[0, 0, 0], *args, **kwargs):
        super(AxisEntity, self).__init__(pos, *args, **kwargs)

    def draw(self):
        self.pre_draw()
        glBegin(GL_LINES)

        # X
        glColor(1, 0, 0)
        glVertex(0, 0, 0)
        glVertex(1, 0, 0)

        # Y
        glColor(0, 1, 0)
        glVertex(0, 0, 0)
        glVertex(0, 1, 0)

        # Z
        glColor(0, 0, 1)
        glVertex(0, 0, 0)
        glVertex(0, 0, 1)

        glEnd()
        self.post_draw()
