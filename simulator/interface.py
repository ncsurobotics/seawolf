
from __future__ import division
import sys
from math import sin, cos, radians, degrees

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Interface(object):

    def __init__(self, cam_pos=(0,0,0), cam_pitch=0, cam_yaw=0):

        self.cam_pos = cam_pos
        self.cam_pitch = cam_pitch  # Degrees
        self.cam_yaw = cam_yaw  # Degrees

        self.camera_modes = [
            "freecam",
            "robot_forward",
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
        glClearColor(0,0,0,0)
        glShadeModel(GL_FLAT)
        glEnable(GL_NORMALIZE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glDisable(GL_CULL_FACE)
        glDisable(GL_BLEND)

        # Lighting
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 0.1))
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, -1, 0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (0.1, 0.1, 0.1, 0.1))
        glLightfv(GL_LIGHT1, GL_POSITION, (0.5, -1, -1, 0))
        glLightfv(GL_LIGHT1, GL_AMBIENT, (0, 0, 0, 1))
        glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))
        glLightfv(GL_LIGHT1, GL_SPECULAR, (0.1, 0.1, 0.1, 0.1))
        #glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

        # Callbacks
        glutDisplayFunc(self.draw)
        glutKeyboardFunc(self.keyboard_callback)
        glutSpecialFunc(self.special_keyboard_callback)
        glutMouseFunc(self.mouse_callback)

        self.init_viewport()

    def run(self, delay):
        glutTimerFunc(0, self.timer_callback, int(1000*delay))
        glutMainLoop()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.init_camera()
        glMatrixMode(GL_MODELVIEW)
        for entity in self.simulator.entities:
            entity.draw()
        glFlush()
        glutSwapBuffers()

    def init_viewport(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, self.view_width, self.view_height)
        gluPerspective(self.fov,
                       self.view_width/self.view_height,  # Aspect ratio
                       0.1, 4000)  # Near and far

    def init_camera(self):

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if self.camera_mode == "freecam":
            # If camera is straight up or down, prevent up vector from being
            # parallel to the viewing angle.
            if abs(self.cam_pitch) >= 90:
                up_vector = (
                    -cos(radians(self.cam_yaw)) * self.cam_pitch/90,
                    -sin(radians(self.cam_yaw)) * self.cam_pitch/90,
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

        elif self.camera_mode == "robot_forward":
            self.simulator.robot.camera_transform("forward")

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
        self.cam_yaw = (self.cam_yaw+yaw) % 360

    def camera_move_forward(self, distance):
        camera_direction = self.get_camera_direction()
        self.cam_pos[0] += distance * camera_direction[0]
        self.cam_pos[1] += distance * camera_direction[1]
        self.cam_pos[2] += distance * camera_direction[2]

    def reshape_callback(self, width, height):
        self.view_width = width
        self.view_height = height
        self.init_viewport()

    def register_simulator(self, simulator):
        self.simulator = simulator

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
        elif key == 'v':  # Cycle camera mode
            current_index = self.camera_modes.index(self.camera_mode)
            next_index = (current_index+1) % len(self.camera_modes)
            self.camera_mode = self.camera_modes[next_index]

    def special_keyboard_callback(self, key, x, y):
        if key == GLUT_KEY_UP:
            self.camera_move_forward(0.1)
        elif key == GLUT_KEY_DOWN:
            self.camera_move_forward(-0.1)
        elif key == GLUT_KEY_LEFT:
            self.camera_move_yaw(5)
        elif key == GLUT_KEY_RIGHT:
            self.camera_move_yaw(-5)

    def mouse_motion_look_callback(self, x, y):
        self.camera_move_yaw((self.last_mouse_position[0] - x) * 0.5)
        self.camera_move_pitch((self.last_mouse_position[1] - y) * 0.5)
        self.last_mouse_position = (x,y)
        glutPostRedisplay()

    def mouse_motion_move_callback(self, x, y):
        self.camera_move_forward((self.last_mouse_position[1] - y) * 0.1)
        self.last_mouse_position = (x,y)
        glutPostRedisplay()

    def mouse_callback(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.last_mouse_position = (x,y)
                glutMotionFunc(self.mouse_motion_look_callback)
                self.left_mouse_down = True
            else:
                glutMotionFunc(None)
                self.left_mouse_down = False

        elif button == GLUT_MIDDLE_BUTTON:
            if state == GLUT_DOWN:
                self.last_mouse_position = (x,y)
                glutMotionFunc(self.mouse_motion_move_callback)
                self.left_mouse_down = True
            else:
                glutMotionFunc(None)
                self.left_mouse_down = False
