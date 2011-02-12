
from __future__ import division
import math
from collections import deque

from missions.base import MissionBase
import entities
import sw3

# If the path's position is off by more than this much, turn towards it
RHO_CENTERING_THRESHOLD = 20  # pixel distance
THETA_CENTERING_THRESHOLD = 100 * (math.pi/180)  # radians

THETA_RECORD_LENGTH = 5  # How many path orientations to keep track of

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

    def init(self):
        self.entity_searcher.start_search([
            entities.PathEntity(),
        ])
        sw3.nav.do(sw3.Forward(0.3))

    def step(self, entity_found):
        if self.orienting: return

        x = entity_found.center[0]
        y = entity_found.center[1]
        position_rho = math.sqrt(x**2 + y**2)
        position_theta = math.atan2(x, y)

        if position_rho > RHO_CENTERING_THRESHOLD and \
            abs(position_theta) > THETA_CENTERING_THRESHOLD:

            # Point robot toward path, then go forward
            sw3.nav.do(sw3.RelativeYaw(position_theta * (math.pi/180)))
            sw3.nav.append(sw3.Forward(0.3))

        else:
            if y > 0:
                sw3.nav.do(sw3.Forward(0.2))
            else:
                sw3.nav.do(sw3.Forward(-0.2))

        # Collect angle data
        self.orientation_measurements.append(entity_found.theta + sw3.data.imu.yaw * (math.pi/180))

        if len(self.orientation_measurements) == THETA_RECORD_LENGTH and \
            angle_range(self.orientation_measurements) < ORIENTATION_RANGE_THRESHOLD:

            self.start_orientation()

    def start_orientation(self):
        self.entity_searcher.start_search([])
        turn_routine = sw3.SetYaw(angle_average(self.orientation_measurements))
        turn_routine.on_done(self.finish_mission)
        sw3.nav.do(turn_routine)
        print "Orienting!"
        print "Angles:", self.orientation_measurements
        self.orienting = True
