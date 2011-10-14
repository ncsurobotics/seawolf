

from __future__ import division

import entities
from missions.base import MissionBase
from vision import process_manager
import sw3
import math
from math import pi

MISSION_TIMEOUT = 5
DEGREE_PER_PIXEL = 0.10
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = 0.1
CENTERED_THRESHOLD = 0.4
FIELD_OF_VIEW=40

class PathMission(MissionBase):

    def __init__(self, path_type=entities.PATH):
        self.path_type = path_type
        self.path_seen = 0

    def init(self):
        self.process_manager.start_process(entities.PathEntity,"path", "down", debug = True)
        sw3.nav.do(sw3.CompoundRoutine([sw3.Forward(FORWARD_SPEED)]))

        self.reference_angle = sw3.data.imu.yaw*(pi/180) % (2*pi)
        self.depth = sw3.data.depth
        self.state = "centering"


    def step(self, vision_data):

        print vision_data
        path_data = vision_data['path']
        #if isinstance(path_data, process_manager.KillSignal):
        #    raise path_data 

           # gate_center = DEGREE_PER_PIXEL*(gate_data.left_pole + gate_data.right_pole)/2  # degrees
        if self.state == "centering":
                 
        theta_x = path_data.x*FIELD_OF_VIEW*180/pi #path_data.x is percent of fram view . multiplying them gives you theta_x
        theta_y = path_data.y*FIELD_OF_VIEW*180/pi #path_data.y is percent of frame view . multiplying them gives you theta

        d = PATH_DEPTH-depth #depth between path and camera

        x = d*sin(theta_x) #gives you the x distance from the frame center to path center
        y = d*sin(theta_y) #gives you the y distance from the frame center to path center 

    def state_centering(self):
         position_rho = math.sqrt(path_data.x**2+path_data.y**2) #hypotenuse-distance from frame center to path center
         position_phi = math.atan2(path_data.x,path_data.y)*(180/pi) #

    def state_orienting(self)

