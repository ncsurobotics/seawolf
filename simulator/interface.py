
from __future__ import division
import sys
from math import sin, cos, radians, degrees

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy
import cv

import seawolf
import svr


class Interface(object):

    def __init__(self, cam_pos=(0, 0, 0), cam_pitch=0, cam_yaw=0,
                 parameter_sets={}, svr_source=False):

        self.cam_pos = numpy.array(cam_pos, numpy.float)
        self.cam_pitch = cam_pitch  # Degrees
        self.cam_yaw = cam_yaw  # Degrees
        self.last_parameter_set = None
        self.parameter_sets = parameter_sets
        self.svr_source = svr_source
        self.frame_number = 0

        self.camera_modes = [
            "Free Cam",
            "Forward Cam",
            "Down Cam",
        ]
        self.camera_mode = self.camera_modes[0]
        self.simulator = None
        self.left_mouse_down = False
        self.view_width = 800
        self.view_height = 800
        self.fov = 70  # Degrees

        # Window Init
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.view_width, self.view_height)
        glutCreateWindow("Simulator")

        # OpenGL Settings
        glClearColor(0, 0, 0, 0)
        glShadeModel(GL_FLAT)
        glEnable(GL_NORMALIZE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glDisable(GL_CULL_FACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Lighting
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 0.1))
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, -1, 0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (0, 0, 0, 0))
        glLightfv(GL_LIGHT1, GL_POSITION, (0.5, -1, -1, 0))
        glLightfv(GL_LIGHT1, GL_AMBIENT, (0, 0, 0, 1))
        glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))
        glLightfv(GL_LIGHT1, GL_SPECULAR, (0, 0, 0, 0))
        # glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

        # Callbacks
        glutDisplayFunc(self.draw)
        glutKeyboardFunc(self.keyboard_callback)
        glutSpecialFunc(self.special_keyboard_callback)
        glutMouseFunc(self.mouse_callback)

        # Parameter Set Menu
        parameter_set_menu = glutCreateMenu(self.parameter_set_menu_callback)
        for i, set_name in enumerate(self.parameter_sets.iterkeys()):
            glutAddMenuEntry(set_name, i)

        # Camera Mode Menu
        camera_mode_menu = glutCreateMenu(self.camera_mode_callback)
        for i, mode_name in enumerate(self.camera_modes):
            glutAddMenuEntry(mode_name, i)

        # Main menu
        glutCreateMenu(self.main_menu_callback)
        glutAddSubMenu("Reset", parameter_set_menu)
        glutAddSubMenu("Cam Mode", camera_mode_menu)
        glutAddMenuEntry("Zero Thrusters", 2)
        glutAddMenuEntry("Quit", 1)
        glutAttachMenu(GLUT_RIGHT_BUTTON)

        self.init_viewport()

        # Init SVR Sources
        if self.svr_source:
            svr.connect()
            self.svr_sources = {}  # Map camera names to svr sources
            for camera in ["forward", "down"]:
                source = svr.Source(camera)
                source.set_encoding("raw")
                self.svr_sources[camera] = source

    def run(self, delay):
        glutTimerFunc(0, self.timer_callback, int(1000 * delay))
        glutMainLoop()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.init_camera()
        glMatrixMode(GL_MODELVIEW)

        for entity in self.simulator.entities:
            entity.draw()

        # Draw water
        glEnable(GL_BLEND)
        glDepthMask(False)
        glColor(0, 0, 1, 0.2)
        glBegin(GL_QUADS)
        glVertex(-1, -1, 0, 0.001)
        glVertex(-1, 1, 0, 0.001)
        glVertex(1, 1, 0, 0.001)
        glVertex(1, -1, 0, 0.001)
        glEnd()
        glDepthMask(True)
        glDisable(GL_BLEND)

        # Draw Floor
        glColor(0.05, 0.05, 0.05)
        glBegin(GL_QUADS)
        glVertex(-1000, -1000, -16)
        glVertex(-1000, 1000, -16)
        glVertex(1000, 1000, -16)
        glVertex(1000, -1000, -16)
        glEnd()

        glFlush()
        glutSwapBuffers()

        if self.svr_source and self.frame_number % 2 == 0:
            for camera in ["forward", "down"]:

                # Create image and send it
                size = (640, 480)
                fovx = self.simulator.robot.get_camera_fov(camera, False)
                fovy = self.simulator.robot.get_camera_fov(camera, True)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                glViewport(0, 0, size[0], size[1])
                gluPerspective(fovy, fovx / fovy, 0.1, 4000)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                self.simulator.robot.camera_transform(camera)
                for entity in self.simulator.entities:
                    if entity is not self.simulator.robot:
                        entity.draw()
                glFlush()
                data = glReadPixels(0, 0, size[0], size[1], GL_BGR, GL_UNSIGNED_BYTE)
                image = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
                cv.SetData(image, data, 640 * 3)
                cv.Flip(image, flipMode=0)
                self.svr_sources[camera].send_frame(image)

            self.init_viewport()

        self.frame_number += 1

    def init_viewport(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, self.view_width, self.view_height)
        gluPerspective(self.fov,
                       self.view_width / self.view_height,  # Aspect ratio
                       0.1, 4000)  # Near and far

    def init_camera(self):

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if self.camera_mode == "Free Cam":
            # If camera is straight up or down, prevent up vector from being
            # parallel to the viewing angle.
            if abs(self.cam_pitch) >= 90:
                up_vector = (
                    -cos(radians(self.cam_yaw)) * self.cam_pitch / 90,
                    -sin(radians(self.cam_yaw)) * self.cam_pitch / 90,
                    0,
                )
            else:
                up_vector = (0, 0, 1)
            camera_direction = self.get_camera_direction()
            gluLookAt(
                self.cam_pos[0], self.cam_pos[1], self.cam_pos[2],
                self.cam_pos[0] + camera_direction[0],
                self.cam_pos[1] + camera_direction[1],
                self.cam_pos[2] + camera_direction[2],
                up_vector[0], up_vector[1], up_vector[2])

        elif self.camera_mode == "Forward Cam":
            self.simulator.robot.camera_transform("forward")
        elif self.camera_mode == "Down Cam":
            self.simulator.robot.camera_transform("down")
        else:
            raise ValueError("Error: Bad camera mode: " + self.camera_mode)

    def get_camera_direction(self):
        return (
            cos(radians(self.cam_yaw)) * cos(radians(self.cam_pitch)),
            sin(radians(self.cam_yaw)) * cos(radians(self.cam_pitch)),
            sin(radians(self.cam_pitch)),
        )

    def camera_move_pitch(self, pitch):
        self.cam_pitch += pitch
        if self.cam_pitch >= 90:
            self.cam_pitch = 90
        elif self.cam_pitch <= -90:
            self.cam_pitch = -90

    def camera_move_yaw(self, yaw):
        self.cam_yaw = (self.cam_yaw + yaw) % 360

    def camera_move_forward(self, distance):
        camera_direction = self.get_camera_direction()
        self.camera_move(camera_direction, distance)

    def camera_move_right(self, distance):
        right_vector = (
            cos(radians(self.cam_yaw + 90)),
            sin(radians(self.cam_yaw + 90)),
            0,
        )
        self.camera_move(right_vector, distance)

    def camera_move_up(self, distance):
        up_vector = (
            cos(radians(self.cam_yaw)) * sin(radians(-1 * self.cam_pitch)),
            sin(radians(self.cam_yaw)) * sin(radians(-1 * self.cam_pitch)),
            cos(radians(-1 * self.cam_pitch)),
        )
        self.camera_move(up_vector, distance)

    def camera_move(self, direction, distance):
        self.cam_pos[0] += direction[0] * distance
        self.cam_pos[1] += direction[1] * distance
        self.cam_pos[2] += direction[2] * distance

    def register_simulator(self, simulator):
        self.simulator = simulator

    def zero_thrusters(self):
        seawolf.var.set("DepthPID.Paused", 1)
        seawolf.var.set("PitchPID.Paused", 1)
        seawolf.var.set("YawPID.Paused", 1)

        seawolf.notify.send("THRUSTER_REQUEST", "Depth 0 0 0")
        seawolf.notify.send("THRUSTER_REQUEST", "Forward 0 0")

        seawolf.var.set("Port", 0)
        seawolf.var.set("Star", 0)
        seawolf.var.set("Bow", 0)
        seawolf.var.set("Stern", 0)
        seawolf.var.set("StrafeT", 0)
        seawolf.var.set("StrafeB", 0)

    def change_parameter_set(self, set_name):
        self.zero_thrusters()
        parameters = self.parameter_sets[set_name]
        self.last_parameter_set = set_name
        self.simulator.robot.set_pos(parameters['robot_pos'])
        self.simulator.robot.yaw = parameters['robot_yaw']

    ####### Callbacks #######

    def reshape_callback(self, width, height):
        self.view_width = width
        self.view_height = height
        self.init_viewport()

    def timer_callback(self, delay):
        glutTimerFunc(delay, self.timer_callback, delay)
        self.simulator.step()
        glutPostRedisplay()

    def keyboard_callback(self, key, x, y):
        if key == 'u':  # Pitch Up
            self.camera_move_pitch(5)

        elif key == 'd':  # Pitch down
            self.camera_move_pitch(-5)

        elif key == 'f':  # Freecam look forward
            self.cam_yaw = 0
            self.cam_pitch = 0

        elif key == 'm':  # Cycle camera mode
            current_index = self.camera_modes.index(self.camera_mode)
            next_index = (current_index + 1) % len(self.camera_modes)
            self.camera_mode = self.camera_modes[next_index]

        elif key == 'r':  # Reset
            if self.last_parameter_set:
                self.change_parameter_set(self.last_parameter_set)
            else:
                print "No previous reset state.  Cannot reset!  Use the right click menu to reset once before using the shortcut."

        elif key == 'z':  # Zero Thrusters
            self.zero_thrusters()

    def special_keyboard_callback(self, key, x, y):
        if key == GLUT_KEY_UP:
            self.camera_move_forward(0.8)
        elif key == GLUT_KEY_DOWN:
            self.camera_move_forward(-0.8)
        elif key == GLUT_KEY_LEFT:
            self.camera_move_yaw(1)
        elif key == GLUT_KEY_RIGHT:
            self.camera_move_yaw(-1)

    def mouse_motion_look_callback(self, x, y):
        self.camera_move_yaw((self.last_mouse_position[0] - x) * 0.5)
        self.camera_move_pitch((self.last_mouse_position[1] - y) * 0.5)
        self.last_mouse_position = (x, y)
        glutPostRedisplay()

    def mouse_motion_move_callback(self, x, y):
        self.camera_move_right((self.last_mouse_position[0] - x) * 0.1)
        self.camera_move_up((self.last_mouse_position[1] - y) * 0.1)
        self.last_mouse_position = (x, y)
        glutPostRedisplay()

    def mouse_callback(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.last_mouse_position = (x, y)
                glutMotionFunc(self.mouse_motion_look_callback)
                self.left_mouse_down = True
            else:
                glutMotionFunc(None)
                self.left_mouse_down = False

        elif button == GLUT_MIDDLE_BUTTON:
            if state == GLUT_DOWN:
                self.last_mouse_position = (x, y)
                glutMotionFunc(self.mouse_motion_move_callback)
                self.left_mouse_down = True
            else:
                glutMotionFunc(None)
                self.left_mouse_down = False

        # Wheel forward and backward
        # Constants for this seem to be undefined.  They should be
        # GLUT_WHEEL_(UP|DOWN).
        elif state == GLUT_UP and button == 3:
            self.camera_move_forward(1.2)
        elif state == GLUT_UP and button == 4:
            self.camera_move_forward(-1.2)

    def main_menu_callback(self, item):

        if item == 1:  # Quit
            sys.exit(0)

        elif item == 2:  # Zero Thrusters
            self.zero_thrusters()

        return 0

    def parameter_set_menu_callback(self, parameter_set_index):
        set_name = self.parameter_sets.keys()[parameter_set_index]
        self.change_parameter_set(set_name)
        return 0

    def camera_mode_callback(self, mode_index):
        self.camera_mode = self.camera_modes[mode_index]
        return 0
