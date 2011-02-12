
from __future__ import division
import math
from collections import deque

from missions.base import MissionBase
import entities
import sw3

# If the path's position is off by more than this much, turn towards it
RHO_CENTERING_THRESHOLD = 20  # pixel distance
THETA_CENTERING_THRESHOLD = 50 * (math.pi/180)  # radians

THETA_RECORD_LENGTH = 5  # How many path orientations to keep track of


CENTERED_THRESHOLD = 20
# The range of our angle measurements must be less than this to
# start orienting ourselves.
ORIENTATION_RANGE_THRESHOLD = 10 * (math.pi/180)

def angle_range(angles):
    angle_max = angles[0]
    angle_min = angles[0]
    for angle in angles:

        if angle_max < angle:
            angle_max = angle
        if angle_min > angle:
            angle_min = angle

    range = angle_max - angle_min
    if range > math.pi:
        range = math.pi - range
    return range

def angle_average(angles):
    total_x = 0
    total_y = 0
    for angle in angles:
        total_x += math.sin(angle)
        total_y += math.cos(angle)
    return math.atan2(total_x, total_y)

class PathMission(MissionBase):

    def __init__(self):
        self.orientation_measurements = deque(maxlen=THETA_RECORD_LENGTH)
        self.orienting = False
        self.centered_count = 0

    def init(self):
        self.entity_searcher.start_search([
            entities.PathEntity(),
        ])
        sw3.nav.do(sw3.Forward(0.2))

    def step(self, entity_found):
        if self.orienting: return

        x = entity_found.center[0]
        y = entity_found.center[1]
        position_rho = math.sqrt(x**2 + y**2)
        position_theta = math.atan2(x, y)
        position_theta = -(position_theta+math.pi/2)
        if position_theta > math.pi:
            position_theta -= math.pi

        yaw_routine = None
        forward_routine = None

        '''
        if abs(y) >= CENTERED_THRESHOLD and \
            abs(position_theta) > THETA_CENTERING_THRESHOLD:

            # Point robot toward path, then go forward
            yaw_routine = sw3.RelativeYaw(position_theta * (180/math.pi))
            forward_routine = sw3.Forward(0.1)
            print "Correcting Yaw", position_theta * (180/math.pi)
        '''

        if not yaw_routine:
            if y > CENTERED_THRESHOLD:
                forward_routine = sw3.Forward(0.1)
                self.centered_count = 0
                print "Forward"
            elif y < -1*CENTERED_THRESHOLD:
                forward_routine = sw3.Forward(-0.1)
                self.centered_count = 0
                print "Backward"
            else:
                self.centered_count += 1
                forward_routine = sw3.Forward(0.1*y/CENTERED_THRESHOLD)
                print "CENTERED!!!!!!", 0.1*y/CENTERED_THRESHOLD

        # Collect angle data
        #print "Path at theta:", entity_found.theta*(180/math.pi) + sw3.data.imu.yaw
        self.orientation_measurements.append(entity_found.theta + sw3.data.imu.yaw * (math.pi/180))

        if self.centered_count >= 4 and \
            len(self.orientation_measurements) == THETA_RECORD_LENGTH and \
            angle_range(self.orientation_measurements) < ORIENTATION_RANGE_THRESHOLD:

            self.start_orientation()

        else:
            if yaw_routine and forward_routine:
                sw3.nav.do(yaw_routine)
                sw3.nav.append(forward_routine)
            elif yaw_routine:
                sw3.nav.do(yaw_routine)
            elif forward_routine:
                sw3.nav.do(forward_routine)

    def start_orientation(self):
        self.entity_searcher.start_search([])

        turn_routine = sw3.SetYaw((180/math.pi)*angle_average(self.orientation_measurements))
        turn_routine.on_done(self.finish_mission)
        sw3.nav.do(turn_routine)
        sw3.nav.append(sw3.HoldYaw())

        print "Orienting to", angle_average(self.orientation_measurements) *(180/math.pi)
        self.orienting = True
