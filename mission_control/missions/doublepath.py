
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
PREFERED_DIRECTION = 0 #1 is left, -1 is right
CUTOFF_ANGLE = -45 #hard division between paths
CENTERED_THRESHOLD = 60  # pixel distance
THETA_CENTERING_THRESHOLD = 30 * (pi/180)  # radians
CENTERED_FRAMES_THRESHOLD = 3  # Center for this many frames before orientation
PERPENDICULAR_THRESHOLD = pi/8 #how close in radians to perpendicular we expect buoy rods to be

BAD_PATH_ANGLE = -90

# Angle precision and time we must be oriented to finish mission
ORIENT_TIME_THRESHOLD = 3
ORIENT_ANGLE_THRESHOLD = 7
ANGULAR_IDENTIFICATION_THRESHOLD = 10

ORIENT_DELAY = 0.1

class DoublePathMission(MissionBase):

    def __init__(self):
        self.centered_count = 0
        self.last_time_oriented = None

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
        self.known_angle = None
        self.seen_bad_path = False

    def step(self, entity_found):

        #If we see two paths, determine which one is correct
        #and record its abolute angle
        if entity_found and len(entity_found.paths) == 2:
            print "See Two Paths"
            cur_heading = sw3.data.imu.yaw *  pi / 180 
            ang1 = cur_heading + entity_found.paths[0].theta
            ang2 = cur_heading + entity_found.paths[1].theta
            diff1 = abs(util.circular_distance(ang1,self.reference_angle,pi,-pi))
            diff2 = abs(util.circular_distance(ang2,self.reference_angle,pi,-pi))
            if diff1 > pi/2: ang1 += pi
            if diff2 > pi/2: ang2 += pi
            ang1 += pi
            ang2 += pi
            ang1 = ang1 % 2*pi
            ang2 = ang2 % 2*pi
            ang1 -= pi
            ang2 -= pi

            if PREFERED_DIRECTION * (ang1 - ang2) < 0:
                #1st path is our desired path
                target_path = entity_found.paths[0]
                self.known_angle = ang1
            else:
                #2nd path is our desired path
                target_path = entity_found.paths[1]
                self.known_angle = ang2
            print "setting known angle = ", self.known_angle

        #if we see one path, check that it is at an expected angle
        elif entity_found and len(entity_found.paths) == 1:
            print "see one path"
            cur_heading = sw3.data.imu.yaw * pi / 180
            ang = cur_heading + entity_found.paths[0].theta
            diff = abs(util.circular_distance(ang,self.reference_angle,pi,-pi))
            if diff > pi/2: ang += pi
            ang += pi
            ang = ang % 2*pi
            ang -= pi

            if self.known_angle:
                print "alligning wiht known_angle"
                #we have already seen a path we know is correct
                #only track a path if it has a similar angle
                ang_error = abs(util.circular_distance(ang, self.known_angle, pi, -pi))
                if ang_error < ANGULAR_IDENTIFICATION_THRESHOLD:
                    #this is the correct path
                    target_path = entity_found.paths[0]
                    print "path matches known angle"
                else:
                    target_path = None
                    print "path failed known angle"
            else:
                print "using cutoff angle"
                #check to make sure the angle is where we expect
                if ang < CUTOFF_ANGLE:
                    print "path passes cutoff angle"
                    target_path = entity_found.paths[0]
                    self.known_angle = ang
                elif not self.seen_bad_path:
                    print "this is a bad path"
                    #this is not the correct path!! turn 60 degrees
                    #to the left and flag that we have turned
                    self.seen_bad_path = True
                    sw3.nav.do(sw3.RelativeYaw(BAD_PATH_ANGLE))
                    target_path = None
                else:
                    #hopefully we will see the correct path soon
                    print "see nothing or a bad path"
                    target_path = None

        #we see no paths, or more than two paths
        else:
            target_path = None

        #copy imu data to target path
        if target_path:
            target_path.current_yaw = entity_found.current_yaw

        #if we see a valid target, run path as normal

        if self.state == "centering":
            if target_path and self.state_centering(target_path):
                print "Orienting Now"
                self.state = "orienting"
            else:
                return False
        if self.state == "orienting":
            self.set_entity_timeout(0.2)
            finished = self.state_orienting(target_path)
            return finished

    def state_orienting(self, entity_found):

        # Update orientation if path is seen
        t = time()
        if not self.last_time_oriented or (entity_found and t-self.last_time_oriented > ORIENT_DELAY):
            self.last_time_oriented = t

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

        elif not entity_found:
            print "Not orienting because of delay"

        desired_yaw = seawolf.var.get("YawPID.Heading")
        error = util.circular_distance(desired_yaw, sw3.data.imu.yaw, 180, -180)
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
