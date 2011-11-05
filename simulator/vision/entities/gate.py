
from OpenGL.GL import *
from OpenGL.GLU import *

from base import Entity, Container

class GateEntity(Entity):

    def __init__(self, *args, **kwargs):
        super(GateEntity, self).__init__(*args, **kwargs)
        self.image_width = 640

    def draw(self):
        self.pre_draw()
        glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1,0.5,0))
        glMatrixMode(GL_MODELVIEW)

        # Right Pole
        glPushMatrix()
        glTranslate(0, 5, -6)
        gluCylinder(gluNewQuadric(), 0.2, 0.2, 6, 10, 1)
        glPopMatrix()

        # Left Pole
        glPushMatrix()
        glTranslate(0, -5, -6)
        gluCylinder(gluNewQuadric(), 0.2, 0.2, 6, 10, 1)
        glPopMatrix()

        # Cross Pole
        glPushMatrix()
        glTranslate(0, 5, 0)
        glRotate(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 0.2, 0.2, 10, 10, 1)
        glPopMatrix()

        self.post_draw()

    def find(self, robot):
        c = Container()
        c.left_pole = robot.find_point("forward", self.absolute_point((0, 5)))
        c.right_pole = robot.find_point("forward", self.absolute_point((0, -5)))
        if c.left_pole:
            c.left_pole *= self.image_width/2
        if c.right_pole:
            c.right_pole *= self.image_width/2
        return c
