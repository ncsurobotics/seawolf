
from __future__ import division
from time import time, sleep
from math import sin, cos, radians, degrees
import sys
import socket
from multiprocessing.connection import Listener

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from vision import entities
import model

class Simulator(object):

    def __init__(self, robot_pos=[0,0,0], robot_yaw=0, bind_address="localhost", bind_port=3829):

        self.entities = []
        self.bind_address = bind_address
        self.bind_port = bind_port

        self.previous_time = None
        self.graphics_initialized = False

        self.view_width = 400
        self.view_height = 400
        self.fov = 70  # Degrees

        self.cam_pos = [0,0,0]
        self.cam_pitch = 0  # Degrees
        self.cam_yaw = 0  # Degrees

        self.left_mouse_down = False

        self.init_graphics()

        self.robot = entities.RobotEntity(
            model.ObjModel(file("models/seawolf5.obj")),
            pos = robot_pos,
            yaw_offset = -90,
            yaw = robot_yaw,
        )
        self.add_entity(self.robot)

        self.searching_entities = []
        self.last_capture_time = time()
        self.camera_frame_rate = 2

        # Listen for mission control on socket
        self.listener = Listener((self.bind_address, self.bind_port))
        self.listener._listener._socket.settimeout(0.01)  # Nonblocking self.listener..accept

        # Connection to mission control
        self.connection = None

    def add_entity(self, entity):
        entity._register_simulator(self)
        self.entities.append(entity)

    def add_entities(self, entities):
        self.entities.extend(entities)

    def handle_pipe(self):

        # Attempt connection if not connected
        if self.connection is None:
            try:
                self.connection = self.listener.accept()
            except socket.timeout:
                self.connection = None

        # Get new entity search list
        if self.connection:
            try:
                while self.connection.poll():
                    self.searching_entities = self.connection.recv()
            except EOFError:
                # Other end has closed
                self.searching_entities = []
                self.connection = None

    def entity_search(self):

        # Only capture every 1/self.camera_frame_rate secs
        t = time()
        if t < self.last_capture_time + 1/self.camera_frame_rate:
            return
        self.last_capture_time = t

        # Call entity.find for each entity
        data_list = []
        for entity in self.searching_entities:
            entity_data = self.robot.find_entity(entity)
            if entity_data:
                data_list.append( (entity, entity_data) )

        if data_list:
            self.connection.send(data_list)

    def run(self, delay=0.05):
        self.delay = delay
        self.previous_time = time()

        glutMainLoop()

    def step(self, dt=None):

        self.handle_pipe()
        self.entity_search()

        t = time()
        if not dt:
            dt = t - self.previous_time

        for entity in self.entities:
            entity.step(dt)

        self.previous_time = t


    ####################### Graphics #######################
    # Camera starts at the origin looking down the +X axis.  This is yaw=0
    # pitch=0 and position=0,0,0.  +Z is up.

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.init_camera()
        glMatrixMode(GL_MODELVIEW)
        for entity in self.entities:
            entity.draw()
        glFlush()
        glutSwapBuffers()

    def init_graphics(self):

        # Only run once
        if self.graphics_initialized:
            return
        else:
            self.graphics_initialized = True

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
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.4, 0.4, 0.4, 0.1))
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, -1, 0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (0.1, 0.1, 0.1, 0.1))
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Callbacks
        glutDisplayFunc(self.draw)
        glutTimerFunc(0, self.timer_callback, 0)
        glutKeyboardFunc(self.keyboard_callback)
        glutSpecialFunc(self.special_keyboard_callback)
        glutMouseFunc(self.mouse_callback)

        self.init_viewport()

    def init_viewport(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, self.view_width, self.view_height)
        gluPerspective(self.fov,
                       self.view_width/self.view_height,  # Aspect ratio
                       1, 4000)  # Near and far

    def init_camera(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
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

    def timer_callback(self, value=None):
        glutTimerFunc(int(self.delay*1000), self.timer_callback, 0)
        self.step()
        glutPostRedisplay()

    def keyboard_callback(self, key, x, y):
        if key == 'u':
            self.camera_move_pitch(5)
        elif key == 'd':
            self.camera_move_pitch(-5)
        elif key == 'f':
            self.cam_yaw = 0
            self.cam_pitch = 0

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

