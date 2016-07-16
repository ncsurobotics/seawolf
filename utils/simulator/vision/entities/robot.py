
from __future__ import division
from math import radians, degrees, sin, cos, pi, atan2, tan
import numpy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import seawolf

from base import Entity
from doublepath import DoublePathEntity
import model


class RobotEntity(Entity):

    DEPTH_CONSTANT = 1.5
    VELOCITY_CONSTANT = 1
    YAW_CONSTANT = 40

    def __init__(self, *args, **kwargs):
        super(RobotEntity, self).__init__(*args, **kwargs)

        self.yaw_offset = 90

        #self.model = model.ObjModel(file("models/seawolf5.obj"))
        self.model = model.StlModel("models/seawolf6.stl", ambient=(1, 0, 0, 0), diffuse=(1, 0, 0, 0))

        self.depth = -1 * self.pos[2]
        self.tracked_vars = {}

        seawolf.var.subscribe("Port")
        seawolf.var.subscribe("Star")
        seawolf.var.subscribe("Bow")
        seawolf.var.subscribe("Stern")
        seawolf.var.subscribe("StrafeT")
        seawolf.var.subscribe("StrafeB")

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
        strafeT = self.get_var("StrafeT")
        strafeB = self.get_var("StrafeB")
        
        # Velocity
        velocity_fw     = (port + star) * self.VELOCITY_CONSTANT
        velocity_stf    = (strafeT - strafeB) * self.VELOCITY_CONSTANT
        velocity_dph    = (bow + stern) * self.DEPTH_CONSTANT
        
        # IMU
        pitch = -self.pitch #IMU convention: pitch --- Simulator convention: self.pitch

        # Depth
        self.depth      = -self.pos[2]
        self.depth      += dt * velocity_dph
        if self.depth < 0:
            self.depth  += 1.0 * dt
        self.pos[2]     = -1 * self.depth
        seawolf.var.set("Depth", self.depth)

        # Position
        self.pos[0] += dt * (cos(radians(-self.yaw)) * sin(radians(pitch + 90)) * velocity_fw 
                           + sin(radians(-self.yaw)) * sin(radians(self.roll  + 90)) * velocity_stf
                           + cos(radians(-self.yaw)) * sin(radians(pitch))      * velocity_dph)
                           
        self.pos[1] += dt * (sin(radians(-self.yaw)) * sin(radians(pitch + 90)) * velocity_fw
                           + -cos(radians(-self.yaw)) * sin(radians(self.roll  + 90)) * velocity_stf
                           + sin(radians(-self.yaw)) * sin(radians(pitch))      * velocity_dph)


        # Yaw
        self.yaw = self.yaw + (port - star) * self.YAW_CONSTANT * dt
        self.yaw = (self.yaw + 180) % 360 - 180  # Range -180 to 180
        seawolf.var.set("SEA.Yaw", self.yaw)
        seawolf.notify.send("UPDATED", "IMU")
        
        # Pitch

    def draw(self):
        self.pre_draw()

        # Account for model offsets and draw the model
        glPushMatrix()
        glRotate(self.yaw_offset, 0, 0, -1)
        self.model.draw()
        glPopMatrix()

        # Down camera guides
        glColor(1, 1, 0, 0.2)
        glPushMatrix()
        glTranslate(0.0, 0, -0.60)
        glRotate(90, 0, 1, 0)
        self.draw_camera_guides(
            self.get_camera_fov("down", vertical=False),
            self.get_camera_fov("down", vertical=True)
        )
        glPopMatrix()

        # Forward camera guides
        glColor(0, 1, 0, 0.2)
        glTranslate(1.1, 0, 0)
        self.draw_camera_guides(
            self.get_camera_fov("forward", vertical=False),
            self.get_camera_fov("forward", vertical=True)
        )

        self.post_draw()

    def draw_camera_guides(self, horizontal_fov, vertical_fov, box_dist=4):

        half_horizontal_fov = radians(horizontal_fov) / 2
        half_vertical_fov = radians(vertical_fov) / 2

        right = tan(half_horizontal_fov) * box_dist
        left = -right
        top = tan(half_vertical_fov) * box_dist
        bottom = -top

        # Draw box
        glBegin(GL_LINE_LOOP)
        glVertex(box_dist, left, top)
        glVertex(box_dist, right, top)
        glVertex(box_dist, right, bottom)
        glVertex(box_dist, left, bottom)
        glEnd()

        glBegin(GL_LINES)

        # Middle line
        glVertex(0, 0, 0)
        glVertex(box_dist, 0, 0)

        # Lines from box to camera
        glVertex(0, 0, 0)
        glVertex(box_dist, left, top)
        glVertex(0, 0, 0)
        glVertex(box_dist, right, top)
        glVertex(0, 0, 0)
        glVertex(box_dist, right, bottom)
        glVertex(0, 0, 0)
        glVertex(box_dist, left, bottom)

        glEnd()

        # Fill in the fruscum
        # Enable blending for transparency effect.  Disable writing to depth
        # buffer with glDepthMask so objects that are behind this will still be
        # drawn.
        blend_setting = glGetBooleanv(GL_BLEND)
        glEnable(GL_BLEND)
        glDepthMask(False)
        glBegin(GL_TRIANGLE_FAN)
        glVertex(0, 0, 0)
        glVertex(box_dist, left, top)
        glVertex(box_dist, right, top)
        glVertex(box_dist, right, bottom)
        glVertex(box_dist, left, bottom)
        glVertex(box_dist, left, top)
        glEnd()
        glDepthMask(True)
        if not blend_setting:
            glDisable(GL_BLEND)

    def find_entity(self, entity_cls):

        if entity_cls == DoublePathEntity:
            return DoublePathEntity.find_paths(self, self.simulator.entities)

        data = None
        entity_class_found = False
        for entity in self.simulator.entities:
            if entity.__class__.__name__ == entity_cls.__name__:

                entity_class_found = True
                found, data = entity.find(self)
                if found:
                    break

        if not entity_class_found:
            print "Warning: Entity %s is being searched for, but none exists in the simulator." % entity_cls

        return data

    def find_point(self, camera, point):
        '''Finds a point viewed from the given camera.

        All angles that are returned are expressed as a number from -1 to 1.  0
        is straight ahead, -1 is maximum fov to the left or down, 1 is maximum
        fov to the right or up.

        '''

        # Convert to homogeneous coordinates (column matrix)
        if len(point) == 3:
            dimmensions = 3
            point = numpy.matrix([point[0], point[1], point[2], 1]).transpose()
        elif len(point) == 2:
            dimmensions = 2
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
        phi = degrees(atan2(new_point[1], -new_point[2]))

        # Scale from -fov to fov
        half_horizontal_fov = self.get_camera_fov(camera, vertical=False) / 2
        half_vertical_fov = self.get_camera_fov(camera, vertical=True) / 2
        theta = theta / half_horizontal_fov
        phi = phi / half_vertical_fov

        # Make None if outside fov
        if abs(theta) > 1:
            theta = None
        if abs(phi) > 1:
            phi = None

        if dimmensions == 2:
            return theta
        else:
            return theta, phi

    def get_camera_fov(self, camera, vertical=False):
        # All cameras are currently the same
        if vertical:
            return 52  # TODO: We've never measured this, so this is a guess
        else:
            return 68

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
            ref_point = self.absolute_point((1.6, 0, 0))
            cam_point = self.absolute_point((1.1, 0, 0))
            up = self.absolute_point((0, 0, 1)) - self.pos

        elif camera == "down":
            cam_point = self.absolute_point((0, 0, -0.6))
            ref_point = self.absolute_point((0, 0, -1.6))
            up = self.absolute_point((1, 0, 0)) - self.pos

        else:
            raise ValueError('Unknown camera: "%s"' % camera)

        gluLookAt(
            cam_point[0], cam_point[1], cam_point[2],
            ref_point[0], ref_point[1], ref_point[2],
            up[0], up[1], up[2])
