
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
        self.output.buoys = []
        self.id_counter = 0

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

        self.output.buoys = filter(lambda x:x.found, self.output.buoys)
        for buoy in self.output.buoys:
            buoy.found = False

        new_buoys = []
        for pos, color in izip(self.positions, self.color_names):
            theta, phi = robot.find_point("forward", self.absolute_point(pos))
            if theta != None and phi != None:
                theta *= robot.get_camera_fov("forward", vertical=False)/2
                phi *= robot.get_camera_fov("forward", vertical=True)/2

                # Find existing bouy with similar theta and phi
                similar_buoy_found = False
                for buoy in self.output.buoys:
                    if buoy.color == color:
                        similar_buoy_found = True
                        buoy.theta = theta
                        buoy.phi = phi
                        buoy.found = True
                        break

                # Create new buoy
                if not similar_buoy_found:
                    buoy = Container()
                    buoy.theta = theta
                    buoy.phi = phi
                    buoy.id = self.id_counter
                    self.id_counter += 1
                    buoy.color = color
                    buoy.found = True
                    new_buoys.append(buoy)

        self.output.buoys.extend(new_buoys)
        return self.output
