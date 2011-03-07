
from __future__ import division
import math
from math import pi
from collections import deque

from missions.base import MissionBase
import entities
import sw3
from sw3 import util

# If the path's position is off by more than this much, turn towards it
CENTERED_THRESHOLD = 60  # pixel distance
THETA_CENTERING_THRESHOLD = 30 * (pi/180)  # radians
CENTERED_FRAMES_THRESHOLD = 3  # Center for this many frames before orientation

class PathMission(MissionBase):

    def __init__(self):
        self.orienting = False
        self.centered_count = 0

    def init(self):
        self.entity_searcher.start_search([
            entities.PathEntity(),
        ])
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Forward(0.4), sw3.SetDepth(2)
        ]))

        self.reference_angle = sw3.data.imu.yaw*(pi/180) % (2*pi)
        self.oriented = 0

    def step(self, entity_found):
        if self.orienting: return False

        x = entity_found.center[0]
        y = entity_found.center[1]
        position_rho = math.sqrt(x**2 + y**2)
        position_theta = math.atan2(x, y)

        yaw_routine = None
        forward_routine = None

        if abs(y) >= CENTERED_THRESHOLD and \
            abs(position_theta) > THETA_CENTERING_THRESHOLD:

            # Point robot toward path, then go forward
            yaw_routine = sw3.RelativeYaw(position_theta * (180/pi))
            forward_routine = sw3.Forward(0.3)
            print "Correcting Yaw", position_theta * (180/pi)

        if not yaw_routine:
            if y > CENTERED_THRESHOLD:
                forward_routine = sw3.Forward(0.3)
                self.centered_count = 0
                print "Forward"
            elif y < -1*CENTERED_THRESHOLD:
                forward_routine = sw3.Forward(-0.3)
                self.centered_count = 0
                print "Backward"
            else:
                self.centered_count += 1
                forward_routine = sw3.Forward(0.1*y/CENTERED_THRESHOLD)
                print "Centered for:", self.centered_count

        if self.centered_count >= CENTERED_FRAMES_THRESHOLD:

            # Get current yaw
            current_yaw = (sw3.data.imu.yaw*(pi/180)) % (2*pi)

            absolute_path_angle = (entity_found.theta + current_yaw) % pi
            self.start_orientation(absolute_path_angle)
            return False

        if yaw_routine and forward_routine:
            sw3.nav.do(yaw_routine)
            sw3.nav.append(forward_routine)
        elif yaw_routine:
            sw3.nav.do(yaw_routine)
        elif forward_routine:
            sw3.nav.do(forward_routine)

    def start_orientation(self, path_direction):
        #self.entity_searcher.start_search([])

        # Flip direction if it will make path_direction closer to the reference angle.
        opposite_direction = (pi + path_direction) % (2*pi)
        if util.circular_distance(self.reference_angle, opposite_direction) < util.circular_distance(self.reference_angle, path_direction):
            path_direction = opposite_direction
        if path_direction > math.pi:  # convert to range -pi to pi
            path_direction = path_direction - 2*pi

        print "Orienting to", (180/pi)*path_direction
        turn_routine = sw3.SetYaw((180/pi)*path_direction)
        turn_routine.on_done(self.finish_mission)
        sw3.nav.do(turn_routine)

        self.orienting = True
