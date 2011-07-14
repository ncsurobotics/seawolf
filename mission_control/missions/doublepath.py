
from __future__ import division
import math
from math import pi
from collections import deque
from time import time

from missions.base import MissionBase
import entities
import sw3
from sw3 import util
import seawolf

# If the path's position is off by more than this much, turn towards it
CENTERED_THRESHOLD = 60  # pixel distance
THETA_CENTERING_THRESHOLD = 30 * (pi/180)  # radians
CENTERED_FRAMES_THRESHOLD = 3  # Center for this many frames before orientation
PERPENDICULAR_THRESHOLD = pi/8 #how close in radians to perpendicular we expect buoy rods to be

# Angle precision and time we must be oriented to finish mission
ORIENT_TIME_THRESHOLD = 3
ORIENT_ANGLE_THRESHOLD = 7

class DoublePathMission(MissionBase):

    def __init__(self):
        self.centered_count = 0

    def init(self):
        self.entity_searcher.start_search([
            entities.DoublePathEntity(),
        ])
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.Forward(0.4),
            #sw3.SetDepth(2),
        ]))

        # Angle we start the mission at
        self.reference_angle = sw3.data.imu.yaw*(pi/180) % (2*pi)

        self.state = "centering"
        self.orient_time = None

    def step(self, entity_found):

        #If we see two paths, determine which one is correct
        #and record its abolute angle
        if len(entity_found.paths) == 2:
            cur_heading = sw3.data.imu.yaw *  pi / 180 
            ang1 = cur_heading + entity_found.paths[0].theta
            ang2 = cur_heading + entity_found.paths[1].theta
            diff1 = abs(util.circular_distance(ang1,self.reference_angle,pi,-pi))
            diff2 = abs(util.circular_distance(ang2,self.reference_angle,pi,-pi))
            if diff1 > pi/2: ang1 += pi
            if diff2 > pi/2: ang2 += pi
            ang1 = ang1 % 2*pi
            ang2 = ang2 % 2*pi

            if PREFERED_DIRECTION * (diff1 - diff2) < 0:
                #1st path is our desired path
                target_path = entity_found.paths[0]
                self.known_angle = ang1
            else:
                #2nd path is our desired path
                target_path = entity_found.paths[1]
                self.known_angle = ang2

        #if we see one path, check that it is at an expected angle
        elif len(entity_found.paths) == 1:
            cur_heading = sw3.data.imu.yaw * pi / 180
            ang = cur_heading + entity_found.paths[0].theta
            diff = abs(util.circular_distance(ang,self.reference_angle,pi,-pi))
            if diff > pi/2: ang += pi
            ang += pi
            ang = ang % 2*pi
            ang -= pi

            if self.known_angle:
                #we have already seen a path we know is correct
                #only track a path if it has a similar angle
                ang_error = abs(util.circular_distance(ang, self.known_angle, pi, -pi))
                if ang_error < ANGULAR_IDENTIFICATION_THRESHOLD:
                    #this is the correct path
                    target_path = entity_found.paths[0]
                else:
                    target_path = None
            else:
                #check to make sure the angle is where we expect
                if ang < CUTOFF_ANGLE:
                    target_path = entity_found.paths[0]
                    self.known_angle = ang
                elif not self.seen_bad_path:
                    #this is not the correct path!! turn 60 degrees
                    #to the left and flag that we have turned
                    self.seen_bad_path = True
                    sw3.nav.do(sw3.RelativeYaw(-60))
                else:
                    #hopefully we will see the correct path soon
                    target_path = None

        #we see no paths, or more than two paths
        else:
            target_path = None

        #ignore all except for our target path
        self.entity_found = target_path

        #if we see a valid target, run path as normal

        if self.state == "centering":
            if entity_found and self.state_centering(entity_found):
                print "Orienting Now"
                self.state = "orienting"
            else:
                return False
        if self.state == "orienting":
            self.set_entity_timeout(0.2)
            finished = self.state_orienting(entity_found)
            return finished

    def state_orienting(self, entity_found):

        # Update orientation if path is seen
        if entity_found:

            # Get path angle
            current_yaw = (entity_found.current_yaw*(pi/180)) % (2*pi)
            path_angle = (entity_found.theta + current_yaw) % pi

            # Flip direction if it will make path_angle closer to the reference angle.
            opposite_angle = (pi + path_angle) % (2*pi)
            if util.circular_distance(self.reference_angle, opposite_angle) < util.circular_distance(self.reference_angle, path_angle):
                path_angle = opposite_angle
            if path_angle > math.pi:  # convert to range -pi to pi
                path_angle = path_angle - 2*pi

            print "Orienting to", (180/pi)*path_angle
            turn_routine = sw3.SetYaw((180/pi)*path_angle)
            sw3.nav.do(turn_routine)

        desired_yaw = seawolf.var.get("YawPID.Heading")
        error = util.circular_distance(desired_yaw, entity_found.current_yaw, 180, -180)
        print "Angle Error:", error
        t = time()
        if not self.orient_time or error > ORIENT_ANGLE_THRESHOLD:
            self.orient_time = t
        if t - self.orient_time > ORIENT_TIME_THRESHOLD:
            return True
        else:
            return False

    def state_centering(self, entity_found):

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

        # Move to next state when centered
        if self.centered_count >= CENTERED_FRAMES_THRESHOLD:
            return True

        if yaw_routine and forward_routine:
            sw3.nav.do(yaw_routine)
            yaw_routine.on_done(lambda x: sw3.nav.do(forward_routine))
        elif yaw_routine:
            sw3.nav.do(yaw_routine)
        elif forward_routine:
            sw3.nav.do(forward_routine)
