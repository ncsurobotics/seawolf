
from __future__ import division

import entities
from missions.base import MissionBase
import sw3

DEGREE_PER_PIXEL = 0.19
INITIAL_FORWARD_SPEED = 0.3
TRACKING_FORWARD_SPEED = 0.3
MISSION_TIMEOUT = 8

class BuoysMission(MissionBase):

    def __init__(self):
        self.correct_buoy_index = None
        self.seen_count = 0

    def init(self):
        self.entity_searcher.start_search([
            entities.BuoysEntity(),
        ])
        sw3.nav.do(sw3.CompoundRoutine([
            sw3.HoldYaw(), sw3.Forward(INITIAL_FORWARD_SPEED), sw3.SetDepth(2)
        ]))
        self.initial_angle = sw3.data.imu.yaw

    def step(self, entity_found):

        # Complete mission if timeout has passed
        if not entity_found:
            return True

        # Check if this our first time seeing the buoys
        if self.correct_buoy_index is None:

            # Pick out buoy that is most centered
            center_most_location = entity_found.buoy_locations[0]
            self.correct_buoy_index = 0
            for i, location in enumerate(entity_found.buoy_locations):
                if abs(location.x) < center_most_location.x:
                    center_most_location = location
                    self.correct_buoy_index = i

            self.set_entity_timeout(MISSION_TIMEOUT)

        # If center buoy was found, go towards it
        # Do nothing if we've seen it enough already
        location = entity_found.buoy_locations[self.correct_buoy_index]
        if location and self.seen_count < 5:
            print "Moving towards location:", location.x
            self.seen_count += 1
            sw3.nav.do(sw3.CompoundRoutine([
                sw3.RelativeYaw(location.x * DEGREE_PER_PIXEL),
                sw3.Forward(TRACKING_FORWARD_SPEED)
            ]))
