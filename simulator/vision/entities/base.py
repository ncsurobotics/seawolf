
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

    def __init__(self, pos, color=(0.5,0.5,0.5), yaw_offset=0, yaw=0, pitch=0, roll=0):
        assert len(pos)==3
        assert len(color)==3 or len(color)==4
        self.pos = pos
        self.color = color
        self.yaw_offset = yaw_offset
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.simulator = None

    def _register_simulator(self, simulator):
        self.simulator = simulator

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
            #TODO: This doesn't work right!
            raise NotImplementedError()

            # Convert to homogeneous coordinates
            point = numpy.array([point[0], point[1], point[2], 1])

            # Get modelview matrix for this entity
            # Load the identity first so camera positioning doesn't affect this
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            self.pre_draw()
            modelview = glGetDouble(GL_MODELVIEW_MATRIX)
            self.post_draw()
            glPopMatrix()

            # Change from column major to row major
            modelview = modelview.transpose()

            new_point = numpy.dot(point, modelview)
            return new_point[0:3] / new_point[3]

    def pre_draw(self):
        #glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslate(self.pos[0], self.pos[1], self.pos[2])
        glRotate(self.pitch, 0, 1, 0)
        glRotate(self.roll, 1, 0, 0)
        glRotate(self.yaw_offset, 0, 0, -1)
        glRotate(self.yaw, 0, 0, -1)

    def draw(self):
        self.pre_draw()
        self.post_draw()

    def post_draw(self):
        glPopMatrix()

    def find(self, robot):
        raise NotImplementedError("This entity is not searchable.  Implement the find method to add this functionality.")

class ModelEntity(Entity):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(ModelEntity, self).__init__(*args, **kwargs)

    def draw(self):
        self.pre_draw()
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

    def __init__(self, pos=[0,0,0], *args, **kwargs):
        super(AxisEntity, self).__init__(pos, *args, **kwargs)

    def draw(self):
        self.pre_draw()
        glBegin(GL_LINES)

        # X
        glColor(1,0,0)
        glVertex(0,0,0)
        glVertex(1,0,0)

        # Y
        glColor(0,1,0)
        glVertex(0,0,0)
        glVertex(0,1,0)

        # Z
        glColor(0,0,1)
        glVertex(0,0,0)
        glVertex(0,0,1)

        glEnd()
        self.post_draw()
