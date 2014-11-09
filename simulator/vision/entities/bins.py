from __future__ import division
from math import pi, radians

from OpenGL.GL import *
from OpenGL.GLU import *

from base import Entity, Container

BIN_SEPARATION = 0.2
SHAPE_NAMES = [
    "A",
    "B",
    "C",
    "D",
]
BIN_POSITIONS = (
    (
        BIN_SEPARATION + 1,
        -2*BIN_SEPARATION
    ),
    (
        2*BIN_SEPARATION + 3,
        2*BIN_SEPARATION
    ),
    (
        -BIN_SEPARATION - 1,
        2*BIN_SEPARATION
    ),
    (
        -2*BIN_SEPARATION - 3,
        -2*BIN_SEPARATION
    ),
)


class BinsEntity(Entity):

    def __init__(self, *args, **kwargs):
        self.bins_counter = 0
        self.bin_ids = {}
        return super(BinsEntity, self).__init__(*args, **kwargs)

    def draw(self):
        self.pre_draw()
        glMatrixMode(GL_MODELVIEW)

        # For each bin...
        for i in xrange(4):

            glPushMatrix()
            pos = BIN_POSITIONS[i]
            glTranslate(pos[0], pos[1], 0)
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

    def find_bin(self, i, robot):  # I, Robot. The book is 1,000,000 times
                                   # better than the movie
        pos = BIN_POSITIONS[i]
        center = self.absolute_point((pos[0], pos[1], 0))

        b = Container()
        b.theta, b.phi = robot.find_point("down", center)
        b.found = b.theta is not None and b.phi is not None
        b.shape = SHAPE_NAMES[i]

        if b.found:
            if self.bin_ids.get(i, None) is None:
                # Assign new id to bin
                self.bin_ids[i] = self.bins_counter
                self.bins_counter += 1
            b.id = self.bin_ids[i]

        else:
            b.id = None
        self.bin_ids[i] = b.id

        return b

    def find(self, robot):
        c = Container()

        bins = [self.find_bin(i, robot) for i in xrange(4)]
        c.bins = filter(lambda b: b.found, bins)

        if len(c.bins) > 0:
            c.orientation = radians(self.yaw-robot.yaw) % pi
            return True, c
        else:
            c.orientation = None
            return False, c
