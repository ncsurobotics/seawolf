
from math import pi, radians
from itertools import izip
import numpy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from base import Entity, Container

class BuoysEntity(Entity):

    def __init__(self, *args, **kwargs):
        self.positions = [
            numpy.array(kwargs.pop("pos_red", (0,0,0))),
            numpy.array(kwargs.pop("pos_green", (0,0,0))),
            numpy.array(kwargs.pop("pos_yellow", (0,0,0))),
        ]
        super(BuoysEntity, self).__init__(*args, **kwargs)
        self.colors = [
            (1,0,0),
            (0,1,0),
            (1,1,0),
        ]
        self.color_names = ("red", "green", "yellow")
        self.output = Container()
        self.output.red = None
        self.output.green = None
        self.output.yellow = None

    def draw(self):
        self.pre_draw()
        glMatrixMode(GL_MODELVIEW)

        for pos, color in izip(self.positions, self.colors):
            glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)
            glPushMatrix()
            glTranslate(*pos)
            glutSolidSphere(0.75, 8, 8)  # 9 inch diameter
            glPopMatrix()

        self.post_draw()

    def find(self, robot):

        for name, pos, color in izip(self.color_names, self.positions, self.colors):
            x, y = robot.find_point("forward", self.absolute_point(pos))
            if x != None and y != None:
                value = Container()
                value.x = x
                value.y = y
            else:
                value = None
            setattr(self.output, name, value)

        return self.output
