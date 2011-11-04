
from math import pi, radians

from OpenGL.GL import *
from OpenGL.GLU import *

from base import Entity, Container

class PathEntity(Entity):

    def __init__(self, *args, **kwargs):
        super(PathEntity, self).__init__(*args, **kwargs)
        self.output = Container()

    def draw(self):
        self.pre_draw()
        glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1,0.5,0))
        glMatrixMode(GL_MODELVIEW)

        glBegin(GL_QUADS)
        glVertex(-2, -0.25, 0)
        glVertex(-2, 0.25, 0)
        glVertex(2, 0.25, 0)
        glVertex(2, -0.25, 0)
        glEnd()

        self.post_draw()

    def find(self, robot):
        x, y = robot.find_point("down", self.absolute_point((0, 0, 0)))
        if x != None and y != None:
            self.output.found = True
            self.output.x = x
            self.output.y = y
            self.output.theta = radians(self.yaw-robot.yaw) % pi
        else:
            self.output.found = False
        return self.output
