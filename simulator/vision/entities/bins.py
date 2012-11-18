
from OpenGL.GL import *
from OpenGL.GLU import *

from base import Entity, Container

BIN_SEPERATION = 0.2


class BinsEntity(Entity):

    def draw(self):
        self.pre_draw()
        glMatrixMode(GL_MODELVIEW)

        # For each bin...
        for i in xrange(4):

            glPushMatrix()
            x_pos = (i - 1.5) * (2 + BIN_SEPERATION)
            glTranslate(x_pos, 0, 0)
            glBegin(GL_QUADS)

            # Middle black square
            glColor(0, 0, 0)
            glVertex(-0.5, -1, 0)
            glVertex(-0.5, 1, 0)
            glVertex(0.5, 1, 0)
            glVertex(0.5, -1, 0)

            glColor(1, 1, 1)

            # Left portion of white border
            glVertex(-1, -1.5, 0)
            glVertex(-1, 1.5, 0)
            glVertex(-0.5, 1.5, 0)
            glVertex(-0.5, -1.5, 0)

            # Right portion of white border
            glVertex(0.5, -1.5, 0)
            glVertex(0.5, 1.5, 0)
            glVertex(1, 1.5, 0)
            glVertex(1, -1.5, 0)

            # Top portion of white border
            glVertex(-0.5, 1.5, 0)
            glVertex(0.5, 1.5, 0)
            glVertex(0.5, 1, 0)
            glVertex(-0.5, 1, 0)

            # Bottom portion of white border
            glVertex(-0.5, -1, 0)
            glVertex(0.5, -1, 0)
            glVertex(0.5, -1.5, 0)
            glVertex(-0.5, -1.5, 0)

            glEnd()
            glPopMatrix()

        self.post_draw()

    def find(self, robot):
        raise NotImplementedError()

        c = Container()
        c.orientation
        c.bins
        c.bins[0].id
        c.bins[0].theta
        c.bins[0].phi
        c.bins[0].thing

        return found, c
