from __future__ import division

from vision import entities
from missions.base import MissionBase
import sw3
import math
from math import pi
from sw3 import util

import seawolf as sw

MISSION_TIMEOUT = 5
DEGREE_PER_PIXEL = 0.10
STRAIGHT_TOLERANCE = 3  # In degrees
FORWARD_SPEED = 0.3
CENTER_THRESHOLD = 3
FIELD_OF_VIEW = 36
PATH_DEPTH = 8
CENTER_TIME = 5
MIN_ANGLE_THRESHOLD = 5
MAX_ANGLE_THRESHOLD = 175
# for which_path, 0 = right, 1 = left


class PathMission(MissionBase):

    def __init__(self, double=False, which_path=0):
        self.which_path = which_path
        self.double = False
        self.path_seen = 0

    def init(self):
        '''runs at start of mission '''
        if self.double:
            self.process_manager.start_process(entities.DoublePathEntity, "path", "down", debug=True)
        else:
            self.process_manager.start_process(entities.PathEntity, "path", "down", debug=True)
        sw3.nav.do(sw3.CompoundRoutine([sw3.Forward(FORWARD_SPEED)]))

        self.reference_angle = sw.var.get("YawPID.Heading") * (pi / 180) % (2 * pi)
        self.state = "centering"
        self.set_timer("path_timeout", 45, self.fail_mission)

    def step(self, vision_data):

        if not vision_data:
            return
        path_data = None
        if self.double:
            if len(vision_data['path'].paths) == 2:
                if vision_data['path'].paths[0].theta + self.reference_angle < vision_data['path'].paths[1].theta + self.reference_angle:
                    if self.which_path == 0:
                        path_data = vision_data['path'].paths[0]
                    if self.which_path == 1:
                        path_data = vision_data['path'].paths[1]
                    print "debug1"
                    print path_data
                    if path_data:
                        return
                if vision_data['path'].paths[1].theta + self.reference_angle < vision_data['path'].paths[0].theta + self.reference_angle:
                    if self.which_path == 0:
                        path_data = vision_data['path'].paths[1]
                    if self.which_path == 1:
                        path_data = vision_data['path'].paths[0]
                    print "debug2"
                    print path_data
                    if not path_data:
                        return
        else:
            if vision_data['path']:
                path_data = vision_data['path']
            print path_data
            if not path_data.found:
                return
        # Ignore path if it isn't close to the expected angle
        """if self.expected_angle is not None:
            current_yaw = sw3.data.imu.yaw()*(pi/180) % (2*pi)
            path_angle = (path_data.theta + current_yaw) % pi
            opposite_angle = (pi + path_angle) % (2*pi)
            absolute_expected_angle = self.reference_angle + self.expected_angle*(pi/180)
            if util.circular_distance(absolute_expected_angle, path_angle) > self.expected_angle_threshold and \
               util.circular_distance(absolute_expected_angle, opposite_angle) > self.expected_angle_threshold:

                print "Ignoring path out of range"
                return"""
        if path_data:
            theta_x = path_data.x * FIELD_OF_VIEW * pi / 180  # path_data.x is percent of fram view . multiplying them gives you theta_x
            theta_y = path_data.y * FIELD_OF_VIEW * pi / 180  # path_data.y is percent of frame view . multiplying them gives you theta

            d = PATH_DEPTH - sw3.data.depth()  # depth between path and camera

            x = d * math.sin(theta_x)  # g1ves you the x distance from the frame center to path center
            y = d * math.sin(theta_y)  # gives you the y distance from the frame center to path center

            print "Status:Step   x ", x, "   y ", y

            if self.state == "centering":
                self.state_centering(x, y)
            if self.state == "orienting":
                return self.state_orienting(path_data)

    def state_centering(self, x, y):
        position_rho = math.sqrt(x ** 2 + y ** 2)  # hypotenuse-distance from frame center to path center
        position_phi = math.atan2(x, y) * (180 / pi)  # angle of center of path from current position
        print "State:Centering  dist ", position_rho, "  angle from current ", position_phi

        sw3.nav.do(sw3.Forward(0))
        yaw_routine = sw3.RelativeYaw(position_phi)
        forward_routine = sw3.Forward(FORWARD_SPEED, CENTER_TIME)
        sw3.nav.do(yaw_routine)
        yaw_routine.on_done(lambda x: sw3.nav.do(forward_routine))

        if position_rho <= CENTER_THRESHOLD:
            self.state = "orienting"

    def state_orienting(self, path_data):
        current_yaw = sw3.data.imu.yaw() * (pi / 180) % (2 * pi)
        path_angle = (path_data.theta + current_yaw) % pi

        sw3.nav.do(sw3.Forward(0))
        opposite_angle = (pi + path_angle) % (2 * pi)

        print "Status: Orienting   yaw ", current_yaw, " path_angle ", path_angle, " opposite_angle ", opposite_angle

        if util.circular_distance(self.reference_angle, opposite_angle) < util.circular_distance(self.reference_angle, path_angle):
            path_angle = opposite_angle

        if path_angle > math.pi:
            path_angle = path_angle - 2 * pi

        print "Orienting to", (180 / pi) * path_angle
        routine = sw3.SetYaw((180 / pi) * path_angle, timeout=15)
        routine.on_done(self.finish_mission)
        sw3.nav.do(routine)
        self.state = 'done'

        degree = path_data.theta * (180 / pi)

        # if degree <=  MIN_ANGLE_THRESHOLD or degree >= MAX_ANGLE_THRESHOLD:
        '''
        if degree <=  MIN_ANGLE_THRESHOLD:
            self.finish_mission()
        '''
